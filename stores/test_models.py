from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from django.urls import reverse

from django_jsonsaver import constants as c, factories as f, helpers as h
from stores.models import JsonStore

UserModel = get_user_model()


class JsonStoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_model = JsonStore
        cls.test_user = f.UserFactory(username=c.TEST_USER_USERNAME)
        cls.test_jsonstore = JsonStore.objects.create(
            user=cls.test_user,
            name=c.TEST_JSONSTORE_NAME,
            data=c.TEST_JSONSTORE_DATA)

    # ATTRIBUTES #
    def test_model_class_name(self):
        self.assertEqual(self.test_model.__name__, 'JsonStore')

    def test_model_parent_class_name(self):
        self.assertEqual(self.test_model.__bases__[0].__name__, 'Model')

    # FIELDS #

    # user
    def test_field_user_verbose_name(self):
        verbose_name = self.test_jsonstore._meta.get_field('user').verbose_name
        self.assertEqual(verbose_name, 'user')

    def test_field_user_field_type(self):
        field_type = \
            self.test_jsonstore._meta.get_field('user').get_internal_type()
        self.assertEqual(field_type, 'ForeignKey')

    def test_field_user_related_model(self):
        related_model = \
            self.test_jsonstore._meta.get_field('user').related_model
        self.assertEqual(related_model, UserModel)

    def test_field_user_on_delete(self):
        on_delete = \
            self.test_jsonstore._meta.get_field('user').remote_field.on_delete
        self.assertTrue(on_delete is models.CASCADE)

    # name
    def test_field_name_verbose_name(self):
        verbose_name = self.test_jsonstore._meta.get_field('name').verbose_name
        self.assertEqual(verbose_name, 'name')

    def test_field_name_field_type(self):
        field_type = \
            self.test_jsonstore._meta.get_field('name').get_internal_type()
        self.assertEqual(field_type, 'CharField')

    def test_field_name_max_length(self):
        max_length = self.test_jsonstore._meta.get_field('name').max_length
        self.assertEqual(max_length, 128)

    def test_field_name_blank(self):
        blank = self.test_jsonstore._meta.get_field('name').blank
        self.assertEqual(blank, True)

    def test_field_name_null(self):
        null = self.test_jsonstore._meta.get_field('name').null
        self.assertEqual(null, True)

    def test_field_name_help_text(self):
        help_text = self.test_jsonstore._meta.get_field('name').help_text
        self.assertEqual(help_text, c.MODEL_JSONSTORE_NAME_HELP_TEXT)

    # data
    def test_field_data_verbose_name(self):
        verbose_name = self.test_jsonstore._meta.get_field('data').verbose_name
        self.assertEqual(verbose_name, 'data')

    def test_field_data_field_type(self):
        field_type = \
            self.test_jsonstore._meta.get_field('data').get_internal_type()
        self.assertEqual(field_type, 'JSONField')

    def test_field_data_default(self):
        default = self.test_jsonstore._meta.get_field('data').default
        self.assertEqual(default, dict)

    def test_field_data_blank(self):
        blank = self.test_jsonstore._meta.get_field('data').blank
        self.assertEqual(blank, True)

    # is_public
    def test_field_is_public_verbose_name(self):
        verbose_name = \
            self.test_jsonstore._meta.get_field('is_public').verbose_name
        self.assertEqual(verbose_name, 'is public')

    def test_field_is_public_field_type(self):
        field_type = self.test_jsonstore._meta.get_field(
            'is_public').get_internal_type()
        self.assertEqual(field_type, 'BooleanField')

    def test_field_is_public_default(self):
        default = self.test_jsonstore._meta.get_field('is_public').default
        self.assertEqual(default, False)

    def test_field_is_public_help_text(self):
        help_text = self.test_jsonstore._meta.get_field('is_public').help_text
        self.assertEqual(help_text, c.MODEL_JSONSTORE_IS_PUBLIC_HELP_TEXT)

    # updated_at
    def test_field_updated_at_verbose_name(self):
        verbose_name = \
            self.test_jsonstore._meta.get_field('updated_at').verbose_name
        self.assertEqual(verbose_name, 'updated at')

    def test_field_updated_at_field_type(self):
        field_type = self.test_jsonstore._meta.get_field(
            'updated_at').get_internal_type()
        self.assertEqual(field_type, 'DateTimeField')

    def test_field_updated_at_auto_now(self):
        auto_now = self.test_jsonstore._meta.get_field(
            'updated_at').auto_now
        self.assertEqual(auto_now, True)

    # METHODS #

    # __str__()
    def test_method_str_with_name_populated(self):
        expected_string = f"id: {self.test_jsonstore.id}, "\
            f"user: {self.test_jsonstore.user.username}, "\
            f"name: {self.test_jsonstore.name}, "\
            f"is_public: {self.test_jsonstore.is_public}"
        self.assertEqual(str(self.test_jsonstore), expected_string)

    def test_method_str_with_name_blank(self):
        test_jsonstore_with_empty_name = \
            f.JsonStoreFactory(user=self.test_user, name='')
        expected_string = f"id: {test_jsonstore_with_empty_name.id}, "\
            f"user: {test_jsonstore_with_empty_name.user.username}, "\
            f"name: N/A, "\
            f"is_public: {test_jsonstore_with_empty_name.is_public}"
        self.assertEqual(str(test_jsonstore_with_empty_name), expected_string)

    # get_absolute_url()
    def test_get_absolute_url(self):
        expected_url = reverse('stores:jsonstore_detail', kwargs={
            'jsonstore_pk': self.test_jsonstore.pk})
        self.assertEqual(self.test_jsonstore.get_absolute_url(), expected_url)

    def test_get_data_size(self):
        self.assertEqual(
            self.test_jsonstore.get_data_size(),
            h.bytes_to_kb(h.get_obj_size(self.test_jsonstore.data)))

    # FUNCTIONAL #
    def test_model_object_content_and_methods(self):
        expected_name = c.TEST_JSONSTORE_NAME
        expected_data = c.TEST_JSONSTORE_DATA

        # content
        self.assertEqual(self.test_jsonstore.user, self.test_user)
        self.assertEqual(repr(self.test_jsonstore.data), repr(expected_data))
        self.assertEqual(self.test_jsonstore.name, expected_name)
        self.assertEqual(self.test_jsonstore.is_public, False)

        self.assertEqual(
            self.test_jsonstore.get_absolute_url(),
            reverse('stores:jsonstore_detail', kwargs={
                'jsonstore_pk': self.test_jsonstore.pk}))
