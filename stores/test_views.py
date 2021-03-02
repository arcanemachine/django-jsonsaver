import types
from django.test import TestCase
from django.urls import reverse
from html import unescape
from mock import Mock

from django_jsonsaver import constants as c, factories as f
from . import views


class SetUpTestCaseMixin:
    def setUp(self):
        self.client.login(username=self.test_user.username,
                          password=c.TEST_USER_PASSWORD)
        self.response = self.client.get(self.current_test_url)
        self.context = self.response.context
        self.html = unescape(self.response.content.decode('utf-8'))
        self.view_instance = self.response.context['view']


class JsonStoreListViewTest(SetUpTestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.current_test_url = reverse('stores:jsonstore_list')
        cls.view = views.JsonStoreListView

    # request.GET
    def test_request_get(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed('stores/jsonstore_list.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreListView')

    def test_view_mixins(self):
        self.assertEqual(self.view.__bases__[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[1].__name__, 'ListView')

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
        qs_repr = \
            repr(self.test_user.jsonstore_set.order_by('-updated_at'))
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
        cls.test_user = f.UserFactory()
        cls.current_test_url = reverse('stores:jsonstore_create')
        cls.view = views.JsonStoreCreateView

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreCreateView')

    def test_view_mixins(self):
        self.assertEqual(self.view.__bases__[0].__name__, 'LoginRequiredMixin')
        self.assertEqual(
            self.view.__bases__[1].__name__, 'SuccessMessageMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[2].__name__, 'CreateView')

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
        form = Mock()  # create mocked form
        obj = types.SimpleNamespace()  # create dummy object
        obj.save = Mock(return_value=None)  # with dummy return value
        obj.get_absolute_url = Mock(return_value='/')  # returns dummy url
        form.save = Mock(return_value=obj)  # mock the form's save method
        self.view_instance.form_valid(form)  # pass dummy form into form_valid
        self.assertEqual(self.view_instance.object.user, self.test_user)

    # TEMPLATE

    # def test_user_with_max_jsonstore_count_shows_alert(self):
