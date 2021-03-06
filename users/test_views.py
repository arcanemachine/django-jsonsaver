from django.conf import settings
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from . import views
from django_jsonsaver import \
    constants as c, factories as f, helpers_testing as ht
from stores.models import JsonStore

UserModel = get_user_model()


class UsersRootViewTest(SimpleTestCase):
    def setUp(self):
        self.view = views.users_root
        self.test_url = reverse('users:users_root')

    # ATTRIBUTES
    def test_view_function_name(self):
        self.assertEqual(self.view.__name__, 'users_root')

    def test_view_function_args(self):
        args = ht.get_function_args(self.view)
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], 'request')

    # request.GET
    def test_request_get_method_unauthenticated_user_with_requestfactory(self):
        request = RequestFactory().get(self.test_url)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_detail_me'))

    def test_request_get_method_unauthenticated_user_with_client(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_detail_me'))


class UserRegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:register')

    def setUp(self):
        self.view = views.UserRegisterView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserRegisterView')

    def test_view_parent_class(self):
        self.assertEqual(
            self.view.__bases__[-1].__name__, 'CreateView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'NewUserCreationForm')

    def test_view_template_name(self):
        self.assertEqual(self.view.template_name, 'users/register.html')

    def test_view_success_url(self):
        self.assertEqual(self.view.success_url, reverse(settings.LOGIN_URL))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

    # METHODS #

    # dispatch()
    def test_method_dispatch_redirects_authenticated_user(self):
        test_user = f.UserFactory()
        request = RequestFactory().get(self.test_url)
        request.user = test_user
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGIN_URL))

    # form_valid()
    def test_method_form_valid_redirects_if_honeypot_field_present(self):
        old_user_count = UserModel.objects.count()

        # create form
        form = self.view.form_class
        form_data = {'username': c.TEST_USER_USERNAME,
                     'email': c.TEST_USER_EMAIL,
                     'name': c.TEST_USER_FULL_NAME,
                     'password1': c.TEST_USER_PASSWORD,
                     'password2': c.TEST_USER_PASSWORD,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        form_instance = form(data=form_data)
        self.assertTrue(form_instance.is_valid())

        # build request
        request = RequestFactory().post(self.test_url)
        request.user = AnonymousUser()

        # instantiate view class
        view_instance = self.view()
        view_instance.setup(request)
        with self.settings(DEBUG=True):
            view_instance.form_valid(form_instance)

        # user count has not changed
        new_user_count = UserModel.objects.count()
        self.assertEqual(new_user_count, old_user_count)

        # welcome email not sent
        self.assertEqual(len(mail.outbox), 0)

    # FUNCTIONAL #
    def test_functional_create_new_user_using_requestfactory(self):
        old_user_count = UserModel.objects.count()

        # create form
        form = self.view.form_class
        form_data = {'username': c.TEST_USER_USERNAME,
                     'email': c.TEST_USER_EMAIL,
                     'name': '',
                     'password1': c.TEST_USER_PASSWORD,
                     'password2': c.TEST_USER_PASSWORD,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        form_instance = form(data=form_data)
        self.assertTrue(form_instance.is_valid())

        # build request
        request = RequestFactory().post(self.test_url)
        request.user = AnonymousUser()

        # add support for messages
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # instantiate view class
        view_instance = self.view()
        view_instance.setup(request)
        with self.settings(DEBUG=True):
            response = view_instance.form_valid(form_instance)

        # new user has been created
        new_user_count = UserModel.objects.count()
        self.assertTrue(new_user_count == old_user_count + 1)

        # welcome email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "jsonSaver: Activate your account", mail.outbox[0].subject)

        # user contains expected data
        user = UserModel.objects.last()
        self.assertEqual(user.username, c.TEST_USER_USERNAME)
        self.assertEqual(user.email, c.TEST_USER_EMAIL)
        self.assertEqual(user.is_active, False)

        # response contains proper redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

    def test_functional_create_new_user_using_client(self):
        old_user_count = UserModel.objects.count()

        form_data = {'username': c.TEST_USER_USERNAME,
                     'email': c.TEST_USER_EMAIL,
                     'name': '',
                     'password1': c.TEST_USER_PASSWORD,
                     'password2': c.TEST_USER_PASSWORD,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}

        with self.settings(DEBUG=True):
            response = \
                self.client.post(self.test_url, form_data)

        # new user has been created
        new_user_count = UserModel.objects.count()
        self.assertTrue(new_user_count == old_user_count + 1)

        # welcome email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "jsonSaver: Activate your account", mail.outbox[0].subject)

        # user contains expected data
        user = UserModel.objects.last()
        self.assertEqual(user.username, c.TEST_USER_USERNAME)
        self.assertEqual(user.email, c.TEST_USER_EMAIL)
        self.assertEqual(user.is_active, False)

        # response contains proper redirect and success message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_REGISTER_SUCCESS_MESSAGE)


class UserActivationEmailResendViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:user_activation_email_resend')

    def setUp(self):
        self.view = views.UserActivationEmailResendView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserActivationEmailResendView')

    def test_view_parent_class(self):
        self.assertEqual(
            self.view.__bases__[-1].__name__, 'FormView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'UserActivationEmailResendForm')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_activation_email_resend.html')

    def test_view_success_url(self):
        self.assertEqual(self.view.success_url, reverse(settings.LOGIN_URL))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

    # METHODS #

    # form_valid()
    def test_method_form_valid_notify_user_if_account_already_active(self):
        self.test_user = f.UserFactory()

        form_data = {'email': self.test_user.email,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        with self.settings(DEBUG=True):
            response = self.client.post(self.test_url, form_data)

        # response contains proper redirect and success message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            c.USER_VIEW_ACTIVATION_EMAIL_RESEND_ACCOUNT_ALREADY_ACTIVE)

    def test_method_form_valid_send_email_if_user_account_not_activated(self):
        self.test_user = f.UserFactory(is_active=False)

        form_data = {'email': self.test_user.email,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        with self.settings(DEBUG=True):
            response = self.client.post(self.test_url, form_data)

        # response contains proper redirect and success message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            c.USER_VIEW_ACTIVATION_EMAIL_RESEND_SUCCESS_MESSAGE)

        # welcome email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "jsonSaver: Activate your account", mail.outbox[0].subject)

    def test_method_form_valid_enter_invalid_email_address(self):
        form_data = {'email': 'fake@email.com',
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        with self.settings(DEBUG=True):
            response = self.client.post(self.test_url, form_data)

        # response contains proper redirect and success message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            c.USER_VIEW_ACTIVATION_EMAIL_RESEND_SUCCESS_MESSAGE)

        # no email has been sent
        self.assertEqual(len(mail.outbox), 0)


class UserActivateViewTest(TestCase):
    def setUp(self):
        self.view = views.user_activate
        self.test_user = f.UserFactory(is_active=False)
        self.test_url = reverse('users:user_activate', kwargs={
            'activation_code': self.test_user.profile.activation_code})
        self.success_url = reverse(settings.LOGIN_URL)

    # ATTRIBUTES
    def test_view_function_name(self):
        self.assertEqual(self.view.__name__, 'user_activate')

    def test_view_function_args(self):
        args = ht.get_function_args(self.view)
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0], 'request')
        self.assertEqual(args[1], 'activation_code')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_USER_ACTIVATE_SUCCESS_MESSAGE)

        # response redirects to success_url
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGIN_URL))

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)

        # response contains account_already_active message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_USER_ACTIVATE_ACCOUNT_ALREADY_ACTIVE)

    def test_request_get_method_unauthenticated_user_bad_kwargs(self):
        self.test_url = reverse('users:user_activate', kwargs={
            'activation_code': 'bad_kwargs'})
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 404)

    # FUNCTIONAL #
    def test_successful_activation_removes_activation_code(self):
        # activation code present before activation
        self.assertTrue(self.test_user.profile.activation_code is not None)
        self.client.get(self.test_url)

        # activation code no longer present after activation
        self.test_user.profile.refresh_from_db()
        self.assertTrue(self.test_user.profile.activation_code is None)

    def test_successful_activation_adds_status_is_active_to_user(self):
        self.assertFalse(self.test_user.is_active)
        self.client.get(self.test_url)
        self.test_user.refresh_from_db()
        self.assertTrue(self.test_user.is_active)


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.view = views.UserLoginView
        self.test_url = reverse('users:login')

    # ATTRIBUTES
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserLoginView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(mixins[0].__name__, 'SuccessMessageMixin')
        self.assertEqual(len(mixins[:-1]), 1)

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'LoginView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'UserAuthenticationForm')

    def test_view_template_name(self):
        self.assertEqual(self.view.template_name, 'users/login.html')

    def test_view_redirect_authenticated_user(self):
        self.assertEqual(self.view.redirect_authenticated_user, True)

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message, c.USER_VIEW_LOGIN_SUCCESS_MESSAGE)

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGIN_REDIRECT_URL))

    # METHODS #

    # post()
    def test_method_post_unactivated_user_is_notified_and_redirected(self):
        test_user = f.UserFactory(is_active=False)
        form_data = {'username': test_user.username}
        response = self.client.post(self.test_url, form_data)

        # user receives message to activate their account
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_LOGIN_ACTIVATE_ACCOUNT_REMINDER)

        # user is redirected to UserActivationEmailResendView
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse('users:user_activation_email_resend'))

    # FUNCTIONAL #
    def test_login(self):
        test_user = f.UserFactory()
        form_data = {'username': test_user.username,
                     'password': c.TEST_USER_PASSWORD,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        response = self.client.post(
            self.test_url, form_data)

        # user is logged in and redirected to UserDetailMe
        self.assertEqual(response.wsgi_request.user, test_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_detail_me'))


class UserDetailMeViewTest(TestCase):
    def setUp(self):
        self.view = views.UserDetailMeView
        self.test_url = reverse('users:user_detail_me')

    # ATTRIBUTES
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserDetailMeView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(
            self.view.__bases__[0].__name__, 'LoginRequiredMixin')
        self.assertEqual(len(mixins[:-1]), 1)

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DetailView')

    def test_view_template_name(self):
        self.assertEqual(self.view.template_name, 'users/user_detail_me.html')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(self.view.template_name)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS

    # get_context_data
    def test_method_get_object_returns_expected_object_using_client(self):
        test_user = f.UserFactory()
        self.assertTrue(
            self.client.login(username=test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.context['object'], test_user)

    def test_method_get_object_returns_expected_object_as_requestfactory(self):
        test_user = f.UserFactory()
        request = RequestFactory().get(self.test_url)
        request.user = test_user
        view_instance = self.view()
        view_instance.setup(request)
        obj = view_instance.get_object()
        self.assertEqual(obj, test_user)


class UserDetailPublicViewTest(TestCase):
    def setUp(self):
        self.view = views.UserDetailPublicView

        self.test_user = f.UserFactory()
        self.test_user.profile.is_public = True
        self.test_user.profile.save()

        self.test_url = reverse('users:user_detail_public', kwargs={
            'username': self.test_user.username})

    # ATTRIBUTES
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserDetailPublicView')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DetailView')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_detail_public.html')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(
            self.client.login(username=self.test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS #

    # dispatch()
    def test_method_dispatch_profile_is_private_and_user_is_same_user(self):
        self.test_user.profile.is_public = False
        self.test_user.profile.save()

        self.assertTrue(
            self.client.login(username=self.test_user.username,
                              password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        # show account visiblility status message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_DETAIL_PUBLIC_SAME_USER_IS_PRIVATE)

        # redirect to UserUpdateIsPublicView
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_update_is_public'))

    def test_method_dispatch_profile_is_private_and_user_is_other_user(self):
        self.test_user.profile.is_public = False
        self.test_user.profile.save()

        response = self.client.get(self.test_url)

        # return 404
        self.assertEqual(response.status_code, 404)

    # get_context_data()
    def test_get_context_data_returns_expected_jsonstores(self):
        # generate jsonstores
        for i in range(6):
            f.JsonStoreFactory(user=self.test_user, is_public=True)
            f.JsonStoreFactory(is_public=True if i % 2 == 0 else False)
        expected_qs = JsonStore.objects.filter(user=self.test_user) \
            .order_by('-updated_at')

        request = RequestFactory().get(self.test_url)
        request.user = AnonymousUser()
        view_instance = self.view()
        view_instance.setup(request)
        view_instance.kwargs = {'username': self.test_user.username}
        view_instance.object = view_instance.get_object()
        context = view_instance.get_context_data()
        self.assertEqual(repr(context['jsonstores']), repr(expected_qs))

    # get_object()
    def test_get_object_returns_expected_object(self):
        request = RequestFactory().get(self.test_url)
        request.user = AnonymousUser()
        view_instance = self.view()
        view_instance.setup(request)
        view_instance.kwargs = {'username': self.test_user.username}
        obj = view_instance.get_object()
        self.assertEqual(obj, self.test_user)

