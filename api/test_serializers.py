from django.urls import reverse
from mock import Mock
from rest_framework.test import APIRequestFactory, APITestCase

from . import serializers, views
from django_jsonsaver import \
    constants as c, factories as f, helpers as h, server_config as sc


class JsonStoreSerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.view = views.JsonStoreViewSet
        cls.test_serializer = serializers.JsonStoreSerializer
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.test_jsonstore = f.JsonStoreFactory(user=self.test_user)
        self.factory = APIRequestFactory()

    # ATTRIBUTES #
    def test_serializer_class_name(self):
        self.assertEqual(self.test_serializer.__name__, 'JsonStoreSerializer')

    # META #
    def test_meta_model_name(self):
        self.assertEqual(self.test_serializer.Meta.model.__name__, 'JsonStore')

    def test_meta_fields(self):
        self.assertEqual(
            self.test_serializer.Meta.fields,
            ['id', 'user', 'data', 'name', 'is_public'])

    def test_meta_read_only_fields(self):
        self.assertEqual(self.test_serializer.Meta.read_only_fields, ['user'])

    # METHODS #

    # create()
    def test_create_adds_user_to_object(self):
        mocked_self = Mock()
        mocked_self.context = {'request': Mock()}
        mocked_self.context['request'].user = self.test_user
        validated_data = {"data": {},
                          "name": '',
                          "is_public": False}
        result = self.test_serializer.create(mocked_self, validated_data)
        self.assertEqual(result.user, self.test_user)

    # validate_name()
    def test_method_validate_name_slugifies_name(self):
        name = 'Test JsonStore Name'
        slugified_name = self.test_serializer.validate_name(None, name)
        self.assertEqual(slugified_name, 'test-jsonstore-name')

    # VALIDATION #

    def test_validation_jsonstore_public_name_cannot_be_blank(self):
        test_url = reverse('api:jsonstore-list')
        data = {"data": {},
                "name": '',
                "is_public": True}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)
        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK)

    def test_validation_jsonstore_forbidden_name_not_allowed(self):
        test_url = reverse('api:jsonstore-list')
        data = {"data": {},
                "name": c.JSONSTORE_FORBIDDEN_NAMES[0],
                "is_public": False}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        name = serializer.validate_name(data['name'])
        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_FORBIDDEN_NAME_NOT_ALLOWED(name))

    def test_validation_jsonstore_user_jsonstore_count_over_max(self):
        # create stores until user reaches max jsonstore count
        while(self.test_user.jsonstore_set.count() <
                self.test_user.profile.get_max_jsonstore_count()):
            f.JsonStoreFactory(user=self.test_user)

        test_url = reverse('api:jsonstore-list')
        data = {"data": {},
                "name": '',
                "is_public": False}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_USER_JSONSTORE_COUNT_OVER_MAX(
                self.test_user, self.test_user.jsonstore_set.count()))

    def test_validation_jsonstore_name_duplicate_same_user_create(self):
        other_jsonstore = f.JsonStoreFactory(
            user=self.test_user, name='other_jsonstore_name')

        test_url = reverse('api:jsonstore-list')
        data = {"data": {},
                "name": other_jsonstore.name,
                "is_public": False}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE)

    def test_validation_jsonstore_name_duplicate_same_user_update(self):
        other_jsonstore = f.JsonStoreFactory(
            user=self.test_user, name='other_jsonstore_name')

        test_url = reverse('api:jsonstore-detail', kwargs={
            'pk': self.test_jsonstore.pk})

        data = {"name": other_jsonstore.name}
        request = self.factory.patch(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE)

    def test_validation_jsonstore_public_name_duplicate(self):
        other_jsonstore = f.JsonStoreFactory(
            name='other_jsonstore_name',
            is_public=True)

        test_url = reverse('api:jsonstore-list')
        data = {"data": {},
                "name": other_jsonstore.name,
                "is_public": True}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE)

    def test_validation_jsonstore_data_size_over_max(self):
        large_jsonstore_data = 'a' * sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE

        test_url = reverse('api:jsonstore-list')
        data = {"data": large_jsonstore_data,
                "name": '',
                "is_public": False}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
                self.test_user, h.get_obj_size(large_jsonstore_data)))

    def test_validation_all_jsonstores_data_size_over_max(self):
        large_jsonstore_data = \
            'a' * int((sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE / 2))
        f.JsonStoreFactory(user=self.test_user, data=large_jsonstore_data)

        test_url = reverse('api:jsonstore-list')
        data = {"data": large_jsonstore_data,
                "name": '',
                "is_public": False}
        request = self.factory.post(test_url, data)
        request.user = self.test_user
        serializer = \
            self.test_serializer(data=data, context={'request': request})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(len(serializer.errors), 1)
        # self.assertTrue('non_field_errors' in serializer.errors)

        self.assertEqual(
            serializer.errors['non_field_errors'][0].__str__(),
            c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
                self.test_user, h.get_obj_size(large_jsonstore_data)))


class JsonStoreNameSerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_serializer = serializers.JsonStoreNameSerializer

    # ATTRIBUTES #
    def test_serializer_class_name(self):
        self.assertEqual(
            self.test_serializer.__name__, 'JsonStoreNameSerializer')

    # META #
    def test_meta_model_name(self):
        self.assertEqual(self.test_serializer.Meta.model.__name__, 'JsonStore')

    def test_meta_fields(self):
        self.assertEqual(
            self.test_serializer.Meta.fields,
            ['id', 'user', 'data', 'name', 'is_public'])


class JsonStorePublicSerializerTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_serializer = serializers.JsonStorePublicSerializer

    # ATTRIBUTES #
    def test_serializer_class_name(self):
        self.assertEqual(
            self.test_serializer.__name__, 'JsonStorePublicSerializer')

    # META #
    def test_meta_model_name(self):
        self.assertEqual(self.test_serializer.Meta.model.__name__, 'JsonStore')

    def test_meta_fields(self):
        self.assertEqual(self.test_serializer.Meta.fields, ['data', 'name'])

    def test_meta_read_only_fields(self):
        self.assertEqual(
            self.test_serializer.Meta.read_only_fields, ['data', 'name'])
