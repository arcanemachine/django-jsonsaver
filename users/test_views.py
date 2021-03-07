from django.conf import settings
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from . import views
from django_jsonsaver import \
    constants as c, factories as f, helpers_testing as ht, server_config as sc
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
        view_func_args = ht.get_function_args(self.view)
        self.assertEqual(len(view_func_args), 1)
        self.assertEqual(view_func_args[0], 'request')

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
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
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
            f"{sc.PROJECT_NAME}: Activate your account",
            mail.outbox[0].subject)

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
            f"{sc.PROJECT_NAME}: Activate your account",
            mail.outbox[0].subject)

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
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
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
            f"{sc.PROJECT_NAME}: Activate your account",
            mail.outbox[0].subject)

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
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory(is_active=False)
        cls.test_url = reverse('users:user_activate', kwargs={
            'activation_code': cls.test_user.profile.activation_code})
        cls.success_url = reverse(settings.LOGIN_URL)

    def setUp(self):
        self.view = views.user_activate

    # ATTRIBUTES
    def test_view_function_name(self):
        self.assertEqual(self.view.__name__, 'user_activate')

    def test_view_function_args(self):
        view_func_args = ht.get_function_args(self.view)
        self.assertEqual(len(view_func_args), 2)
        self.assertEqual(view_func_args[0], 'request')
        self.assertEqual(view_func_args[1], 'activation_code')

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
        active_user = f.UserFactory()
        self.assertTrue(self.client.login(
            username=active_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)

        # response contains account_already_active message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_USER_ACTIVATE_ACCOUNT_ALREADY_ACTIVE)

    # bad kwargs
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

    def test_successful_activation_creates_user_api_token(self):
        old_token_count = Token.objects.count()
        self.client.get(self.test_url)
        new_token_count = Token.objects.count()
        self.assertEqual(new_token_count, old_token_count + 1)


class UserLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:login')

    def setUp(self):
        self.view = views.UserLoginView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserLoginView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'SuccessMessageMixin')

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
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
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


class UserUsernameRecoverViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:user_username_recover')
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.view = views.UserUsernameRecoverView
        self.form_data = {'email': self.test_user.email,
                          'captcha_0': 'test',
                          'captcha_1': 'PASSED'}

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUsernameRecoverView')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'FormView')

    def test_view_form_class_name(self):
        self.assertEqual(
            self.view.form_class.__name__, 'UserUsernameRecoverForm')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_username_recover.html')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message,
            c.USER_VIEW_USERNAME_RECOVER_SUCCESS_MESSAGE)

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.view.template_name)

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

    # METHODS #

    # dispatch()
    def test_method_dispatch_redirects_authenticated_user(self):
        request = RequestFactory().get(self.test_url)
        request.user = self.test_user
        response = self.view.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

    # form_valid()
    def test_method_form_valid(self):
        # covered by test_user_username_recover_existing_username
        pass

    # FUNCTIONAL #
    def test_user_username_recover_existing_username(self):
        with self.settings(DEBUG=True):
            response = self.client.post(self.test_url, self.form_data)

        # get response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # user_username_recover email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            f"{sc.PROJECT_NAME}: Forgot your username?",
            mail.outbox[0].subject)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_USERNAME_RECOVER_SUCCESS_MESSAGE)

    def test_user_username_recover_non_existent_user_email(self):
        self.form_data.update({'email': 'non_existent_user@email.com'})
        response = self.client.post(self.test_url, self.form_data)

        # get response
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_USERNAME_RECOVER_SUCCESS_MESSAGE)


class UserLogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:logout')
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.view = views.UserLogoutView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserLogoutView')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'LogoutView')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message, c.USER_VIEW_LOGOUT_SUCCESS_MESSAGE)

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGOUT_REDIRECT_URL))

    def test_request_get_method_authenticated_user(self):
        test_user = f.UserFactory()
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.LOGOUT_REDIRECT_URL))

    # METHODS #

    # dispatch()
    def test_method_dispatch_passes_success_message(self):
        response = self.client.get(self.test_url)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), c.USER_VIEW_LOGOUT_SUCCESS_MESSAGE)

    # FUNCTIONAL #
    def test_logout(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))

        # get user information from dummy response objects
        self.assertEqual(self.client.get('/').context['user'], self.test_user)
        self.client.get(self.test_url)
        self.assertEqual(self.client.get('/').context['user'], AnonymousUser())


class UserDetailMeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_url = reverse('users:user_detail_me')

    def setUp(self):
        self.view = views.UserDetailMeView

    # ATTRIBUTES
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserDetailMeView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(self.view.__bases__[0].__name__, 'LoginRequiredMixin')

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
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS

    # get_context_data
    def test_method_get_object_returns_expected_object_using_client(self):
        test_user = f.UserFactory()
        self.assertTrue(self.client.login(
            username=test_user.username, password=c.TEST_USER_PASSWORD))
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
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_user.profile.is_public = True
        cls.test_user.profile.save()
        cls.test_url = reverse('users:user_detail_public', kwargs={
            'username': cls.test_user.username})

    def setUp(self):
        self.view = views.UserDetailPublicView

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
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
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


class UserUpdateTemplateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_user.profile.is_public = True
        cls.test_user.profile.save()
        cls.test_url = reverse('users:user_update')

    def setUp(self):
        self.view = views.UserUpdateTemplateView

    # ATTRIBUTES
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUpdateTemplateView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 2)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')
        self.assertEqual(mixins[1].__name__, 'SuccessMessageMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'TemplateView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'Profile')

    def test_view_template_name(self):
        self.assertEqual(self.view.template_name, 'users/user_update.html')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)


class UserUpdateAccountTierViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('users:user_update_account_tier')

    def setUp(self):
        self.view = views.UserUpdateAccountTierView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUpdateAccountTierView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'TemplateView')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_update_account_tier.html')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)


class UserUpdateEmailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('users:user_update_email')

    def setUp(self):
        self.view = views.UserUpdateEmailView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUpdateEmailView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'FormView')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_update_email.html')

    def test_view_success_url(self):
        self.assertEqual(
            self.view.success_url, reverse('users:user_detail_me'))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS #

    # form_valid()
    def test_method_form_valid(self):
        # old user values
        old_email = self.test_user.email
        new_email = 'new_' + self.test_user.email
        self.assertNotEqual(new_email, old_email)

        # old profile values
        profile = self.test_user.profile
        old_activation_code = profile.activation_code
        self.assertEqual(profile.wants_email, None)

        # get response
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        form_data = {'email': new_email,
                     'captcha_0': 'test',
                     'captcha_1': 'PASSED'}
        with self.settings(DEBUG=True):
            response = self.client.post(self.test_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # user profile is updated as expected
        profile.refresh_from_db()
        self.assertEqual(profile.wants_email, new_email)
        self.assertTrue(profile.activation_code != old_activation_code)
        self.assertIsNotNone(profile.activation_code)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_UPDATE_EMAIL_SUCCESS_MESSAGE)

        # confirmation email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            f"{sc.PROJECT_NAME}: Confirm your new email address",
            mail.outbox[0].subject)

    # get_object()
    def test_get_object_returns_expected_object(self):
        request = RequestFactory().get(self.test_url)
        request.user = self.test_user
        view_instance = self.view()
        view_instance.setup(request)
        obj = view_instance.get_object()
        self.assertEqual(obj, self.test_user.profile)


class UserUpdateEmailConfirmViewTest(TestCase):
    def setUp(self):
        self.view = views.user_update_email_confirm

        # simulate the first step of user_email_update
        self.test_user = f.UserFactory()
        self.new_email = 'new_' + self.test_user.email
        self.test_user.profile.wants_email = self.new_email
        self.test_user.profile.save()
        # use existing activation code instead of generating a new one
        # as would normally happen during the email updating process
        self.test_url = reverse('users:user_update_email_confirm', kwargs={
            'activation_code': self.test_user.profile.activation_code})

    # ATTRIBUTES
    def test_view_function_name(self):
        self.assertEqual(self.view.__name__, 'user_update_email_confirm')

    def test_view_function_args(self):
        view_func_args = ht.get_function_args(self.view)
        self.assertEqual(len(view_func_args), 2)
        self.assertEqual(view_func_args[0], 'request')
        self.assertEqual(view_func_args[1], 'activation_code')

    def test_view_function_decorators(self):
        decorators = ht.get_function_decorators(self.view)
        self.assertEqual(len(decorators), 1)
        self.assertEqual(decorators[0], '@login_required')

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:user_detail_me"))

    # bad kwargs
    def test_request_get_method_authenticated_user_bad_kwargs(self):
        self.test_url = reverse('users:user_update_email_confirm', kwargs={
            'activation_code': 'bad_kwargs'})

        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 404)

    # FUNCTIONAL #

    # success
    def test_functional_user_update_email_confirm(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        old_user_email = self.test_user.email
        old_profile_wants_email = self.test_user.profile.wants_email
        old_profile_activation_code = self.test_user.profile.wants_email

        # expected values updated
        self.test_user.refresh_from_db()
        # email is self.new_email
        self.assertNotEqual(self.test_user.email, old_user_email)
        self.assertEqual(self.test_user.email, self.new_email)
        # profile.wants_email is now None
        self.assertNotEqual(
            old_profile_wants_email, self.test_user.profile.wants_email)
        self.assertEqual(self.test_user.profile.wants_email, None)
        # profile.activation_code is now None
        self.assertNotEqual(old_profile_activation_code, None)
        self.assertEqual(self.test_user.profile.activation_code, None)

        # page redirects as expected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:user_detail_me"))


class UserUpdateIsPublicViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('users:user_update_is_public')

    def setUp(self):
        self.view = views.UserUpdateIsPublicView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUpdateIsPublicView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 2)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')
        self.assertEqual(mixins[1].__name__, 'SuccessMessageMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'UpdateView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'Profile')

    def test_view_fields(self):
        self.assertEqual(self.view.fields, ('is_public',))

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_update_is_public.html')

    def test_view_success_message(self):
        self.assertEqual(
            self.view.success_message,
            c.USER_VIEW_UPDATE_IS_PUBLIC_SUCCESS_MESSAGE)

    def test_view_success_url(self):
        self.assertEqual(
            self.view.success_url, reverse('users:user_detail_me'))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS #

    # get_object()
    def test_get_object_returns_expected_object(self):
        request = RequestFactory().get(self.test_url)
        request.user = self.test_user
        view_instance = self.view()
        view_instance.setup(request)
        obj = view_instance.get_object()
        self.assertEqual(obj, self.test_user.profile)

    # FUNCTIONAL #

    def test_user_update_is_public(self):
        updated_user = f.UserFactory()
        self.assertFalse(updated_user.profile.is_public)

        # update form data
        form_data = {'is_public': ['on']}
        self.assertTrue(self.client.login(
            username=updated_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.post(self.test_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # user profile.is_public is now True
        updated_user.refresh_from_db()
        self.assertTrue(updated_user.profile.is_public)


class UserUpdateApiKeyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        f.TokenFactory(user=cls.test_user)
        cls.test_url = reverse('users:user_update_api_key')

    def setUp(self):
        self.view = views.UserUpdateApiKeyView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserUpdateApiKeyView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'TemplateView')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_update_api_key.html')

    def test_view_success_url(self):
        self.assertEqual(
            self.view.success_url, reverse('users:user_detail_me'))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS #

    # post()
    def test_method_post(self):
        # get token info before post
        old_token_count = Token.objects.count()
        old_token_pk = self.test_user.auth_token.pk
        old_token_key = self.test_user.auth_token.key

        # get response
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.post(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # get token info after post
        self.test_user.refresh_from_db()
        new_token_pk = self.test_user.auth_token.pk
        new_token_key = self.test_user.auth_token.key

        # new token is different from old token
        self.assertNotEqual(new_token_pk, old_token_pk)
        self.assertNotEqual(new_token_key, old_token_key)

        # old key has been removed
        self.assertFalse(Token.objects.filter(pk=old_token_pk).exists())

        # overall token count has not changed
        self.assertEqual(Token.objects.count(), old_token_count)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            c.USER_VIEW_UPDATE_API_KEY_SUCCESS_MESSAGE(new_token_key))


class UserDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('users:user_delete')

    def setUp(self):
        self.view = views.UserDeleteView

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'UserDeleteView')

    def test_view_mixins(self):
        mixins = self.view.__bases__
        self.assertEqual(len(mixins[:-1]), 1)
        self.assertEqual(mixins[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'DeleteView')

    def test_view_template_name(self):
        self.assertEqual(
            self.view.template_name, 'users/user_delete.html')

    def test_view_success_url(self):
        self.assertEqual(self.view.success_url, reverse('project_root'))

    # request.GET
    def test_request_get_method_unauthenticated_user(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"{reverse(settings.LOGIN_URL)}?next={response.wsgi_request.path}")

    def test_request_get_method_authenticated_user(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.view.template_name)

    # METHODS #

    # delete()
    def test_method_delete_displays_success_message(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.delete(self.test_url)

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_DELETE_SUCCESS_MESSAGE)

    # get_object()
    def test_get_object_returns_expected_object(self):
        request = RequestFactory().get(self.test_url)
        request.user = self.test_user
        view_instance = self.view()
        view_instance.setup(request)
        obj = view_instance.get_object()
        self.assertEqual(obj, self.test_user)

    # FUNCTIONAL #

    def test_user_delete_deletes_user(self):
        # info before delete
        old_user_pk = self.test_user.pk
        old_user_count = UserModel.objects.count()

        # get response
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))
        response = self.client.delete(self.test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.view.success_url)

        # info after delete
        new_user_count = UserModel.objects.count()
        self.assertEqual(new_user_count, old_user_count - 1)
        self.assertFalse(UserModel.objects.filter(pk=old_user_pk).exists())

        # response contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_DELETE_SUCCESS_MESSAGE)
