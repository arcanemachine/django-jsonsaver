from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from . import views
from django_jsonsaver import \
    constants as c, factories as f, helpers_testing as ht


class UserRootViewTest(SimpleTestCase):
    def setUp(self):
        self.view = views.users_root
        self.factory = RequestFactory()
        self.current_test_url = reverse('users:users_root')

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

