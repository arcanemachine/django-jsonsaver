from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase, APIRequestFactory

from django_jsonsaver import factories as f
from api.permissions import HasJsonStorePermissions


class HasJsonStorePermissionsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_permission = HasJsonStorePermissions

        # create users
        cls.unprivileged_user = f.UserFactory()
        cls.permitted_user = f.UserFactory()
        cls.admin_user = f.UserFactory(is_staff=True)

        # create JsonStore object owned by permitted_user
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.permitted_user)

    def setUp(self):
        self.request = APIRequestFactory().get('/')

    def test_non_jsonstore_object_raises_typeerror(self):
        obj = None
        with self.assertRaises(TypeError):
            self.test_permission().has_object_permission(
                self.request, None, obj)

    def test_unauthenticated_user_returns_false(self):
        self.request.user = AnonymousUser()
        obj = self.test_jsonstore
        self.assertFalse(
            self.test_permission().has_object_permission(
                self.request, None, obj))

    def test_unprivileged_user_returns_false(self):
        self.request.user = self.unprivileged_user
        obj = self.test_jsonstore
        self.assertFalse(
            self.test_permission().has_object_permission(
                self.request, None, obj))

    def test_permitted_user_returns_true(self):
        self.request.user = self.permitted_user
        obj = self.test_jsonstore
        self.assertTrue(
            self.test_permission().has_object_permission(
                self.request, None, obj))

    def test_admin_user_returns_true(self):
        self.request.user = self.admin_user
        obj = self.test_jsonstore
        self.assertTrue(
            self.test_permission().has_object_permission(
                self.request, None, obj))
