import inspect

from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from . import views
from django_jsonsaver import factories as f
from stores.models import JsonStore


class ApiRootTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_test_url = reverse('api:api_root')

    def setUp(self):
        self.view = views.api_root
        self.factory = APIRequestFactory()

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'api_root')

    def test_view_args(self):
        args = inspect.getargspec(self.view).args
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0], 'request')

    # request.GET
    def test_get_method_unauthenticated_user_using_client(self):
        response = self.client.get(self.current_test_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('api_generic:schema'))

    def test_get_method_unauthenticated_user_using_request_factory(self):
        request = self.factory.get(self.current_test_url)
        request.user = AnonymousUser()
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('api_generic:schema'))


class JsonStoreViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)

    def setUp(self):
        self.view = views.JsonStoreViewSet
        self.factory = APIRequestFactory()

    # ATTRIBUTES #
    def test_view_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreViewSet')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[-1].__name__, 'ModelViewSet')

    def test_view_queryset(self):
        self.assertEqual(
            repr(self.view.queryset), repr(JsonStore.objects.all()))

    def test_view_serializer_class_name(self):
        self.assertEqual(
            self.view.serializer_class.__name__, 'JsonStoreSerializer')

    def test_view_permission_classes(self):
        self.assertEqual(len(self.view.permission_classes), 2)
        self.assertEqual(
            self.view.permission_classes[0].__name__, 'IsAuthenticated')
        self.assertEqual(
            self.view.permission_classes[1].__name__,
            'HasJsonStorePermissions')

    # METHODS #

