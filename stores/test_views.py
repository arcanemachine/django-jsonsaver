from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from unittest.mock import Mock

from django_jsonsaver import constants as c, factories as f
from django_jsonsaver.helpers_testing import SetUpTestCaseMixin
from . import views


class JsonStoreListViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreListView
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('stores:jsonstore_list')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_list.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreListView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'ListView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_context_object_name(self):
        self.assertEqual(self.view.context_object_name, 'jsonstores')

    def test_view_paginate_by(self):
        self.assertEqual(self.view.paginate_by, c.JSONSTORE_LIST_PAGINATE_BY)

    # METHODS #

    # get_queryset()
    def test_method_get_queryset(self):
        for i in range(3):
            f.JsonStoreFactory(user=self.test_user)
        self.setUp()
        qs_repr = repr(self.test_user.jsonstore_set.order_by('-updated_at'))
        self.assertEqual(repr(self.view_instance.get_queryset()), qs_repr)

    # TEMPLATE #
    def test_small_jsonstore_count_has_no_next_page(self):
        self.assertFalse(self.context['page_obj'].paginator.page(1).has_next())

    def test_large_jsonstore_count_has_next_page(self):
        for i in range(c.JSONSTORE_LIST_PAGINATE_BY + 1):
            f.JsonStoreFactory(user=self.test_user)
        self.setUp()
        self.assertTrue(self.context['page_obj'].paginator.page(1).has_next())


class JsonStoreCreateViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreCreateView
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('stores:jsonstore_create')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_form.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreCreateView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'CreateView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_form_class_name(self):
        self.assertEqual(self.view.form_class.__name__, 'JsonStoreForm')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message, c.JSONSTORE_CREATE_SUCCESS_MESSAGE)

    # METHODS #

    # get_context_data()
    def test_method_get_context_data_action_verb(self):
        context = self.view_instance.get_context_data()
        self.assertIn('action_verb', context)
        self.assertEqual(context['action_verb'], 'Create')

    # get_form_kwargs()
    def test_method_get_form_kwargs_user(self):
        kwargs = self.view_instance.get_form_kwargs()
        self.assertIn('user', kwargs)
        self.assertEqual(kwargs['user'], self.test_user)

    # form_valid()
    def test_method_form_valid_assigns_request_user_to_user(self):
        form = Mock()  # create mock form
        obj = Mock()  # create dummy object
        obj.save = Mock(return_value=None)  # with dummy return value
        obj.get_absolute_url = Mock(return_value='/')  # returns dummy url
        form.save = Mock(return_value=obj)  # mock the form's save method
        self.view_instance.form_valid(form)  # pass dummy form into form_valid
        self.assertEqual(self.view_instance.object.user, self.test_user)

    # TEMPLATES #
    def test_template_shows_alert_for_user_with_max_store_count(self):
        pass


class JsonStoreDetailViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreDetailView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_detail', kwargs={
            'jsonstore_pk': cls.test_jsonstore.pk})

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_detail.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreDetailView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(
            mixins[0].__name__, 'UserHasJsonStorePermissionsMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DetailView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_pk_url_kwarg(self):
        self.assertEqual(self.view.pk_url_kwarg, 'jsonstore_pk')

    def test_jsonstore_with_no_name_returns_200(self):
        test_jsonstore = f.JsonStoreFactory(user=self.test_user, name='')
        test_url = reverse('stores:jsonstore_detail', kwargs={
            'jsonstore_pk': test_jsonstore.pk})

        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(test_url)
        self.assertEqual(response.status_code, 200)


    # TEMPLATES
    def test_template_shows_alert_if_jsonstore_is_public(self):
        pass



class JsonStoreLookupViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreLookupView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_lookup')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_lookup.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreLookupView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'FormView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'JsonStoreLookupForm')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'stores/jsonstore_lookup.html')

    # METHODS #

    # form_valid()
    def test_method_form_valid_redirects_to_expected_url(self):
        form = Mock()
        form.cleaned_data = {'jsonstore_name': c.TEST_JSONSTORE_NAME}
        self.response = self.view_instance.form_valid(form)

        # method return HttpResponseRedirect to expected URL
        self.assertEqual(self.response.status_code, 302)
        expected_url = reverse('stores:jsonstore_detail_name', kwargs={
            'jsonstore_name': form.cleaned_data['jsonstore_name']})
        self.assertEqual(self.response.url, expected_url)


class JsonStoreNameDetailViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreNameDetailView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_detail_name', kwargs={
            'jsonstore_name': cls.test_jsonstore.name})

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreNameDetailView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 2)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')
        self.assertEqual(
            mixins[1].__name__, 'UserHasJsonStorePermissionsMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DetailView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    # METHODS #

    # dispatch()
    def test_method_dispatch_lookup_non_existent_jsonstore_name(self):
        test_url = reverse('stores:jsonstore_detail_name', kwargs={
            'jsonstore_name': 'non_existent_jsonstore_name'})
        self.setUp(test_url=test_url)

        # response contains error message
        messages = list(get_messages(self.response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You do not have a JSON store with that name.")

        # user is redirected to expected url
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, reverse('stores:jsonstore_lookup'))

    # get_object()
    def test_method_get_object_returns_expected_object(self):
        self.assertEqual(self.view_instance.get_object(), self.test_jsonstore)

    # TEMPLATES
    def test_template_shows_alert_if_jsonstore_is_public(self):
        return JsonStoreDetailViewTest \
            .test_template_shows_alert_if_jsonstore_is_public(self)


class JsonStorePublicDetailViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStorePublicDetailView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse(
            'stores:jsonstore_detail_public',
            kwargs={'jsonstore_name': cls.test_jsonstore.name})

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 200)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStorePublicDetailView')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DetailView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    # METHODS #

    # dispatch()
    def test_method_dispatch_lookup_non_existent_jsonstore_name(self):
        test_url = reverse('stores:jsonstore_detail_public', kwargs={
            'jsonstore_name': 'non_existent_jsonstore_name'})
        self.setUp(test_url=test_url)

        # response contains error message
        messages = list(get_messages(self.response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "We could not find a public JSON store with that name.")

        # user is redirected to expected url
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(
            self.response.url, reverse('stores:jsonstore_lookup_public'))

    # get_object()
    def test_method_get_object_returns_expected_object(self):
        self.assertEqual(self.view_instance.get_object(), self.test_jsonstore)

    # TEMPLATES
    def test_template_shows_alert_if_jsonstore_is_public(self):
        return JsonStoreDetailViewTest \
            .test_template_shows_alert_if_jsonstore_is_public(self)


class JsonStorePublicLookupViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStorePublicLookupView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_lookup_public')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 200)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_lookup.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStorePublicLookupView')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'FormView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'JsonStorePublicLookupForm')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'stores/jsonstore_lookup.html')

    # METHODS #

    # form_valid()
    def test_method_form_valid_redirects_to_expected_url(self):
        form = Mock()
        form.cleaned_data = {'jsonstore_name': c.TEST_JSONSTORE_NAME}
        self.response = self.view_instance.form_valid(form)

        # method return HttpResponseRedirect to expected URL
        self.assertEqual(self.response.status_code, 302)
        expected_url = reverse('stores:jsonstore_detail_public', kwargs={
            'jsonstore_name': form.cleaned_data['jsonstore_name']})
        self.assertEqual(self.response.url, expected_url)


class JsonStoreUpdateViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreUpdateView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_update', kwargs={
            'jsonstore_pk': cls.test_jsonstore.pk})

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'stores/jsonstore_form.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreUpdateView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 2)
        self.assertEqual(
            mixins[0].__name__, 'UserHasJsonStorePermissionsMixin')
        self.assertEqual(mixins[1].__name__, 'SuccessMessageMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'UpdateView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_form_class_name(self):
        self.assertEqual(self.view.form_class.__name__, 'JsonStoreForm')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message, c.JSONSTORE_UPDATE_SUCCESS_MESSAGE)

    # METHODS #

    # get_context_data()
    def test_method_get_context_data_action_verb(self):
        context = self.view_instance.get_context_data()
        self.assertIn('action_verb', context)
        self.assertEqual(context['action_verb'], 'Update')

    # get_form_kwargs()
    def test_method_get_form_kwargs_user(self):
        kwargs = self.view_instance.get_form_kwargs()
        self.assertIn('user', kwargs)
        self.assertEqual(kwargs['user'], self.test_user)

    def test_method_get_form_kwargs_obj(self):
        kwargs = self.view_instance.get_form_kwargs()
        self.assertIn('obj', kwargs)
        self.assertEqual(kwargs['obj'], self.test_jsonstore)


class JsonStoreDeleteViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreDeleteView
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)
        cls.test_url = reverse('stores:jsonstore_delete', kwargs={
            'jsonstore_pk': cls.test_jsonstore.pk})

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        self.setUp(auth=False)
        self.assertEqual(self.response.status_code, 302)

    def test_request_get_method_authenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, 'stores/jsonstore_confirm_delete.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreDeleteView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(
            mixins[0].__name__, 'UserHasJsonStorePermissionsMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DeleteView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_pk_url_kwarg(self):
        self.assertEqual(self.view.pk_url_kwarg, 'jsonstore_pk')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message, c.JSONSTORE_DELETE_SUCCESS_MESSAGE)

    def test_view_success_url(self):
        self.assertEqual(
            self.view.success_url, reverse('stores:jsonstore_list'))

    # METHODS #

    # delete()
    def test_method_delete_response_contains_success_message(self):
        # delete test_jsonstore
        self.response = self.client.post(self.test_url)

        # messages contains success_messaage
        messages = list(get_messages(self.response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), c.JSONSTORE_DELETE_SUCCESS_MESSAGE)

    # FUNCTIONAL TESTS #
    def test_functional_delete_jsonstore(self):
        # old_jsonstore_count = JsonStore.objects.count()
        # self.response = self.client.post(self.test_url)
        # new_jsonstore_count = JsonStore.objects.count()
        # self.assertEqual(old_jsonstore_count - 1, new_jsonstore_count)
        pass
