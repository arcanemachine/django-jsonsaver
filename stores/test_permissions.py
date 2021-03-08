from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from unittest.mock import Mock

from .permissions import UserHasJsonStorePermissionsMixin
from django_jsonsaver import factories as f


class UserHasJsonStorePermissionsMixinTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_permission = UserHasJsonStorePermissionsMixin()
        cls.request = RequestFactory().get('/')

        cls.test_user = f.UserFactory()
        cls.jsonstore_user = f.UserFactory()
        cls.admin_user = f.UserFactory(is_staff=True)
        cls.test_object = f.JsonStoreFactory(user=cls.jsonstore_user)

    def setUp(self):
        self.test_permission.get_object = Mock(return_value=self.test_object)

    def test_improper_object_type_raises_typeerror(self):
        self.test_object = None
        self.setUp()
        self.test_permission.request = self.request
        with self.assertRaises(TypeError):
            self.test_permission.test_func(None)

    def test_unauthenticated_user_permissions_returns_false(self):
        self.request.user = AnonymousUser()
        self.test_permission.request = self.request
        self.assertFalse(self.test_permission.test_func(self.test_object))

    def test_authenticated_user_permissions_returns_false(self):
        self.request.user = self.test_user
        self.test_permission.request = self.request
        self.assertFalse(self.test_permission.test_func(self.test_object))

    def test_jsonstore_user_permissions_returns_true(self):
        self.request.user = self.jsonstore_user
        self.test_permission.request = self.request
        self.assertTrue(self.test_permission.test_func(self.test_object))

    def test_admin_user_permissions_returns_true(self):
        self.request.user = self.admin_user
        self.test_permission.request = self.request
        self.assertTrue(self.test_permission.test_func(self.test_object))
