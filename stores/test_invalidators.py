from django.test import SimpleTestCase, TestCase

from . import invalidators as iv
from .models import JsonStore
from django_jsonsaver import \
    constants as c, factories as f, server_config as sc


class JsonStorePublicNameCannotBeBlankTest(SimpleTestCase):
    def test_jsonstore_public_name_cannot_be_blank(self):
        name = ''
        is_public = True

        self.assertTrue(
            iv.jsonstore_public_name_cannot_be_blank(name, is_public))


class JsonStoreForbiddenNameNotAllowedTest(SimpleTestCase):
    def test_jsonstore_forbidden_name_not_allowed(self):
        name = c.JSONSTORE_FORBIDDEN_NAMES[0]

        self.assertTrue(iv.jsonstore_forbidden_name_not_allowed(name))


class JsonstoreUserJsonstoreCountOverMaxTest(TestCase):
    def test_jsonstore_user_jsonstore_count_over_max(self):
        user = f.UserFactory()
        user_max_jsonstore_count = 0

        self.assertTrue(
            iv.jsonstore_user_jsonstore_count_over_max(
                user, user_max_jsonstore_count))


class JsonstoreNameDuplicateSameUserCreateTest(TestCase):
    def test_jsonstore_name_duplicate_same_user_create(self):
        name = c.TEST_JSONSTORE_NAME
        user = f.UserFactory()
        obj = None
        f.JsonStoreFactory(user=user, name=name)
        stores_with_same_name = JsonStore.objects.filter(name=name)

        self.assertTrue(
            iv.jsonstore_name_duplicate_same_user_create(
                name, user, obj, stores_with_same_name))


class JsonstoreNameDuplicateSameUserUpdateTest(TestCase):
    def test_jsonstore_name_duplicate_same_user_update(self):
        name = c.TEST_JSONSTORE_NAME
        user = f.UserFactory()
        obj = f.JsonStoreFactory()

        f.JsonStoreFactory(user=user, name=name)
        stores_with_same_name = JsonStore.objects.filter(name=name)

        self.assertTrue(
            iv.jsonstore_name_duplicate_same_user_update(
                name, user, obj, stores_with_same_name))


class JsonstorePublicNameDuplicateTest(TestCase):
    def test_jsonstore_public_name_duplicate(self):
        name = c.TEST_JSONSTORE_NAME
        is_public = True
        user = f.UserFactory()

        other_user = f.UserFactory()
        f.JsonStoreFactory(user=other_user, name=name, is_public=True)
        stores_with_same_name = JsonStore.objects.filter(name=name)

        self.assertTrue(
            iv.jsonstore_public_name_duplicate(
                name, is_public, user, stores_with_same_name))


class JsonstoreDataSizeOverMaxTest(TestCase):
    def test_jsonstore_data_size_over_max(self):
        jsonstore_data = {}
        user = f.UserFactory()
        jsonstore_data_size = sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE

        self.assertTrue(
            iv.jsonstore_data_size_over_max(
                jsonstore_data, user, jsonstore_data_size))


class AllJsonStoresDataSizeOvermax(TestCase):
    def test_all_jsonstores_data_size_over_max(self):
        user = f.UserFactory()
        jsonstore_data_size = \
            sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE

        self.assertTrue(
            iv.jsonstore_all_jsonstores_data_size_over_max(
                user, jsonstore_data_size))
