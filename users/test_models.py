from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from rest_framework.authtoken.models import Token

from django_jsonsaver import \
    constants as c, factories as f, helpers as h, server_config as sc
from .models import Profile

UserModel = get_user_model()


class UserModelTest(TestCase):
    def test_new_user_creation_triggers_api_token_creation(self):
        self.assertEqual(Token.objects.count(), 0) 
        f.UserFactory()
        self.assertEqual(Token.objects.count(), 1) 


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Profile
        cls.test_user = f.UserFactory()
        cls.test_profile = cls.test_user.profile

    # ATTRIBUTES #
    def test_model_class_name(self):
        self.assertEqual(self.test_model.__name__, 'Profile')

    def test_model_parent_class_name(self):
        self.assertEqual(self.test_model.__bases__[0].__name__, 'Model')

    # FIELDS #

    # user
    def test_field_user_verbose_name(self):
        verbose_name = self.test_profile._meta.get_field('user').verbose_name
        self.assertEqual(verbose_name, 'user')

    def test_field_user_field_type(self):
        field_type = \
            self.test_profile._meta.get_field('user').get_internal_type()
        self.assertEqual(field_type, 'OneToOneField')

    def test_field_user_related_model(self):
        related_model = \
            self.test_profile._meta.get_field('user').related_model
        self.assertEqual(related_model, UserModel)

    def test_field_user_on_delete(self):
        on_delete = \
            self.test_profile._meta.get_field('user').remote_field.on_delete
        self.assertTrue(on_delete is models.CASCADE)

    # activation_code
    def test_field_activation_code_verbose_name(self):
        verbose_name = \
            self.test_profile._meta.get_field('activation_code').verbose_name
        self.assertEqual(verbose_name, 'activation code')

    def test_field_activation_code_field_type(self):
        field_type = self.test_profile._meta.get_field('activation_code') \
            .get_internal_type()
        self.assertEqual(field_type, 'CharField')

    def test_field_activation_code_max_length(self):
        max_length = \
            self.test_profile._meta.get_field('activation_code').max_length
        self.assertEqual(max_length, 128)

    def test_field_activation_code_default(self):
        default = \
            self.test_profile._meta.get_field('activation_code').default
        self.assertEqual(default, self.test_model.get_activation_code)

    def test_field_activation_code_null(self):
        null = self.test_profile._meta.get_field('activation_code').null
        self.assertEqual(null, True)

    # wants_email
    def test_field_wants_email_verbose_name(self):
        verbose_name = \
            self.test_profile._meta.get_field('wants_email').verbose_name
        self.assertEqual(verbose_name, 'wants email')

    def test_field_wants_email_field_type(self):
        field_type = self.test_profile._meta.get_field('wants_email') \
            .__class__.__name__
        self.assertEqual(field_type, 'EmailField')

    def test_field_wants_email_null(self):
        null = self.test_profile._meta.get_field('wants_email').null
        self.assertEqual(null, True)

    # is_public
    def test_field_is_public_verbose_name(self):
        verbose_name = \
            self.test_profile._meta.get_field('is_public').verbose_name
        self.assertEqual(verbose_name, c.PROFILE_MODEL_IS_PUBLIC_VERBOSE_NAME)

    def test_field_is_public_field_type(self):
        field_type = self.test_profile._meta.get_field('is_public') \
            .get_internal_type()
        self.assertEqual(field_type, 'BooleanField')

    def test_field_is_public_help_text(self):
        help_text = self.test_profile._meta.get_field('is_public').help_text
        self.assertEqual(help_text, c.PROFILE_MODEL_IS_PUBLIC_HELP_TEXT)

    def test_field_is_public_default(self):
        default = self.test_profile._meta.get_field('is_public').default
        self.assertEqual(default, False)

    # account_tier
    def test_field_account_tier_verbose_name(self):
        verbose_name = \
            self.test_profile._meta.get_field('account_tier').verbose_name
        self.assertEqual(verbose_name, 'account tier')

    def test_field_account_tier_field_type(self):
        field_type = self.test_profile._meta.get_field('account_tier') \
            .get_internal_type()
        self.assertEqual(field_type, 'CharField')

    def test_field_account_tier_max_length(self):
        max_length = \
            self.test_profile._meta.get_field('account_tier').max_length
        self.assertEqual(max_length, 128)

    def test_field_account_tier_default(self):
        default = self.test_profile._meta.get_field('account_tier').default
        self.assertEqual(default, 'free')

    # METHODS #

    # get_activation_code()
    def test_method_get_activation_code_returns_random_string(self):
        self.assertNotEqual(
            Profile.get_activation_code(), Profile.get_activation_code())

    # get_absolute_url()
    def test_method_get_absolute_url_returns_user_absolute_url(self):
        self.assertEqual(
            self.test_profile.get_absolute_url(),
            self.test_profile.user.get_absolute_url())

    # get_all_jsonstores_data_size()
    def test_method_get_all_jsonstores_data_size(self):
        all_jsonstores_data_size = \
            self.test_profile.get_all_jsonstores_data_size

        # if no jsonstores, return value is 0
        self.assertEqual(all_jsonstores_data_size(), 0)

        # if 1 jsonstore, return value is equal to size of that jsonstore
        first_jsonstore = f.JsonStoreFactory(user=self.test_user)
        first_jsonstore_data_size = h.get_obj_size(first_jsonstore.data)
        self.assertEqual(
            all_jsonstores_data_size(), first_jsonstore_data_size)

        # if 2 jsonstores, return value is equal to sum of both jsonstore sizes
        second_jsonstore = f.JsonStoreFactory(user=self.test_user)
        second_jsonstore_data_size = h.get_obj_size(second_jsonstore.data)
        both_jsonstores_data_size = \
            first_jsonstore_data_size + second_jsonstore_data_size
        self.assertEqual(all_jsonstores_data_size(), both_jsonstores_data_size)

    # get_all_jsonstores_data_size_in_kb()
    def test_method_get_all_jsonstores_data_size_in_kb(self):
        all_jsonstores_data_size_in_kb = \
            self.test_profile.get_all_jsonstores_data_size_in_kb

        # if no jsonstores, return value is 0
        self.assertEqual(all_jsonstores_data_size_in_kb(), 0)

        # if 1 jsonstore, return value is equal to size of that jsonstore
        first_jsonstore = f.JsonStoreFactory(user=self.test_user)
        first_jsonstore_data_size_in_kb = \
            h.bytes_to_kb(h.get_obj_size(first_jsonstore.data))
        first_jsonstore_data_size_in_kb_rounded = \
            round(first_jsonstore_data_size_in_kb, 2)

        self.assertEqual(
            all_jsonstores_data_size_in_kb(),
            first_jsonstore_data_size_in_kb_rounded)

        # if 2 jsonstores, return value is equal to sum of both jsonstore sizes
        second_jsonstore = f.JsonStoreFactory(user=self.test_user)
        second_jsonstore_data_size_in_kb = \
            h.bytes_to_kb(h.get_obj_size(second_jsonstore.data))

        both_jsonstores_data_size_in_kb_rounded = round(
            first_jsonstore_data_size_in_kb +
            second_jsonstore_data_size_in_kb, 2)

        self.assertEqual(
            all_jsonstores_data_size_in_kb(),
            both_jsonstores_data_size_in_kb_rounded)

    # get_max_jsonstore_count()
    def test_method_get_max_jsonstore_count(self):
        expected_value = sc.MAX_JSONSTORE_COUNT_USER_FREE
        self.assertEqual(
            self.test_profile.get_max_jsonstore_count(), expected_value)

    # get_max_jsonstore_data_size()
    def test_method_get_max_jsonstore_data_size(self):
        expected_value = sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE
        self.assertEqual(
            self.test_profile.get_max_jsonstore_data_size(), expected_value)

    # get_max_jsonstore_data_size_in_kb()
    def test_method_get_max_jsonstore_data_size_in_kb(self):
        expected_value = h.bytes_to_kb(sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE)
        self.assertEqual(
            self.test_profile.get_max_jsonstore_data_size_in_kb(),
            expected_value)

    # get_max_all_jsonstores_data_size()
    def test_method_get_max_jsonstore_all_jsonstores_data_size(self):
        expected_value = sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE
        self.assertEqual(
            self.test_profile.get_max_jsonstore_all_jsonstores_data_size(),
            expected_value)

    # get_max_jsonstore_all_jsonstores_data_size_in_kb()
    def test_method_get_max_jsonstore_all_jsonstores_data_size_in_kb(self):
        expected_value = h.bytes_to_kb(
            sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE)
        self.assertEqual(
            self.test_profile.
            get_max_jsonstore_all_jsonstores_data_size_in_kb(),
            expected_value)

    # FUNCTIONAL #
    def test_model_object_content_and_methods(self):
        # create a new profile
        user = UserModel.objects.create()
        user.profile.delete()
        profile = Profile.objects.create(user=user)

        # content
        self.assertEqual(profile.user, user)
        self.assertNotEqual(profile.activation_code, None)
        self.assertEqual(profile.wants_email, None)
        self.assertEqual(profile.is_public, False)
        self.assertEqual(profile.account_tier, 'free')

        # methods
        self.assertEqual(profile.get_absolute_url(), user.get_absolute_url())
        self.assertEqual(profile.get_all_jsonstores_data_size(), 0)
        self.assertEqual(profile.get_all_jsonstores_data_size_in_kb(), 0.00)
        self.assertEqual(
            profile.get_max_jsonstore_count(),
            sc.MAX_JSONSTORE_COUNT_USER_FREE)
        self.assertEqual(
            profile.get_max_jsonstore_data_size(),
            sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE)
        self.assertEqual(
            profile.get_max_jsonstore_data_size_in_kb(),
            h.bytes_to_kb(sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE))
        self.assertEqual(
            profile.get_max_jsonstore_all_jsonstores_data_size(),
            sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE)
        self.assertEqual(
            profile.get_max_jsonstore_all_jsonstores_data_size_in_kb(),
            h.bytes_to_kb(sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE))

    def test_new_user_creation_triggers_user_profile_creation(self):
        old_profile_count = Profile.objects.count()
        f.UserFactory()
        new_profile_count = Profile.objects.count()
        self.assertTrue(new_profile_count == old_profile_count + 1)
