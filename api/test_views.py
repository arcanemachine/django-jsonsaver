import inspect

from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from . import views


class ApiRootTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_test_url = reverse('api:api_root')

    def setUp(self):
        self.view = views.api_root
        self.factory = APIRequestFactory()

    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'api_root')

    def test_view_args(self):
        args = inspect.getargspec(self.view).args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], 'request')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        request = self.factory.get(self.current_test_url)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('api_generic:schema'))
