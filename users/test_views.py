from django.conf import settings
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import resolve, reverse
# from mock import Mock

from . import views
from django_jsonsaver import \
    constants as c, factories as f, helpers_testing as ht

UserModel = get_user_model()


class UserRootViewTest(SimpleTestCase):
    def setUp(self):
        self.view = views.users_root
        self.current_test_url = reverse('users:users_root')
        self.factory = RequestFactory()

    # ATTRIBUTES
    def test_view_function_name(self):
        self.assertEqual(self.view.__name__, 'users_root')

    def test_view_function_args(self):
        args = ht.get_function_args(self.view)
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], 'request')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        request = self.factory.get(self.current_test_url)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_detail_me'))


class UserRegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_test_url = reverse('users:register')
        cls.factory = RequestFactory()

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

    # METHODS #

    # dispatch()
    def test_method_dispatch_redirects_authenticated_user(self):
        test_user = f.UserFactory()
        request = self.factory.get(self.current_test_url)
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
        request = self.factory.post(self.current_test_url)
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
        request = self.factory.post(self.current_test_url)
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
            response = self.client.post(self.current_test_url, form_data)

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

        # TODO: template contains success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), c.USER_VIEW_REGISTER_SUCCESS_MESSAGE)
