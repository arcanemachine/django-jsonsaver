from django.forms import widgets
from django.test import SimpleTestCase, TestCase
from django.utils.text import slugify

from . import forms
from .models import JsonStore
from django_jsonsaver import constants as c, factories as f
from django_jsonsaver.server_config import MAX_STORE_DATA_SIZE_USER_FREE


class JsonStoreFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = forms.JsonStoreForm

        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(
            user=cls.test_user,
            name=f"{c.TEST_JSONSTORE_NAME}_UPDATE")
        cls.form_kwargs_create = {'user': cls.test_user}
        cls.form_kwargs_update = {'user': cls.test_user,
                                  'obj': cls.test_jsonstore}

    def setUp(self):
        self.form_data = {'data': {},
                          'name': '',
                          'is_public': False}

    # META #
    def test_meta_model_name(self):
        self.assertEqual(self.form.Meta.model, JsonStore)

    def test_meta_fields(self):
        self.assertEqual(self.form.Meta.fields, ['data', 'name', 'is_public'])

    def test_meta_widgets(self):
        expected_widgets = {'data': widgets.Textarea}
        self.assertEqual(self.form.Meta.widgets, expected_widgets)

    # METHODS #

    # __init__()
    def test_method_init(self):
        form = \
            forms.JsonStoreForm(user=self.test_user, obj=self.test_jsonstore)
        self.assertEqual(form.user, self.test_user)
        self.assertEqual(form.obj, self.test_jsonstore)

    # clean_name()
    def test_clean_name_returns_slugified_name(self):
        name_to_be_slugified = 'Test JsonStore Name'
        self.form_data.update({'name': name_to_be_slugified})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertEqual(form.clean_name(), slugify(name_to_be_slugified))

    # VALIDATION #

    # clean()
    def test_validation_form_is_valid(self):
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertTrue(form.is_valid())

    def test_validation_public_store_name_cannot_be_blank(self):
        self.form_data.update({'name': '',
                               'is_public': True})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('name', 'public_store_name_cannot_be_blank'))

    def test_validation_forbidden_store_names_not_allowed(self):
        self.form_data.update({'name': c.FORBIDDEN_STORE_NAMES[0]})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('name', 'forbidden_store_name_not_allowed'))

    def test_validation_user_has_too_many_stores(self):
        # create jsonstores until user limit is reached
        while (self.test_user.jsonstore_set.count() <
                self.test_user.profile.get_max_store_count()):
            f.JsonStoreFactory(user=self.test_user)

        # attempt to create a new jsonstore
        self.form_data.update({'name': c.TEST_JSONSTORE_NAME})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('__all__', 'user_has_too_many_stores'))

    def test_validation_store_public_name_duplicate_other_user(self):
        # create other user and jsonstore
        other_user = f.UserFactory()
        other_jsonstore = f.JsonStoreFactory(
            user=other_user,
            name='other_jsonstore_name',
            is_public=True)

        # attempt to create store with duplicate name
        self.form_data.update({
            'name': other_jsonstore.name,
            'is_public': True})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('name', 'store_public_name_duplicate_other_user'))

    def test_validation_store_name_duplicate_same_user_create(self):
        # create other user and jsonstore
        other_jsonstore = f.JsonStoreFactory(
            user=self.test_user,
            name='other_jsonstore_name')

        # attempt to create store with duplicate name
        self.form_data.update({'name': other_jsonstore.name})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('name', 'store_name_duplicate_same_user'))

    def test_validation_store_name_duplicate_same_user_update(self):
        # create other user and jsonstore
        other_jsonstore = f.JsonStoreFactory(
            user=self.test_user,
            name='other_jsonstore_name')

        # attempt to update store with duplicate name
        self.form_data.update({'name': other_jsonstore.name})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_update)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('name', 'store_name_duplicate_same_user'))

    def test_validation_store_data_size_over_max(self):
        self.form_data.update(
            {'data': {'message': 'a' * MAX_STORE_DATA_SIZE_USER_FREE}})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('data', 'store_data_size_over_max'))

    def test_validation_all_stores_data_size_over_max(self):
        almost_oversize_data_dict = \
            {'message': 'a' * (MAX_STORE_DATA_SIZE_USER_FREE - 1024)}
        almost_oversize_jsonstore = f.JsonStoreFactory(
            user=self.test_user,
            data=almost_oversize_data_dict)
        self.form_data.update({'data': almost_oversize_data_dict})
        form = forms.JsonStoreForm(self.form_data, **self.form_kwargs_create)
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.has_error('data', 'all_stores_data_size_over_max'))


class JsonStoreLookupFormTest(SimpleTestCase):
    def setUp(self):
        self.form_instance = forms.JsonStoreLookupForm()

    # FIELDS #
    def test_form_fields_all_present(self):
        fields = [field for field in self.form_instance.fields]
        self.assertIn('jsonstore_name', fields)
        self.assertEqual(len(fields), 1)

    # jsonstore_name
    def test_field_jsonstore_name_field_type(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].__class__.__name__,
            'CharField')

    def test_field_jsonstore_name_label(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].label,
            c.STORES_JSONSTORE_LOOKUP_FORM_LABEL)

    def test_field_jsonstore_name_max_length(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].max_length,
            c.JSONSTORE_NAME_MAX_LENGTH)

    def test_field_jsonstore_name_max_help_text(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].help_text,
            c.STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT)


class JsonStorePublicLookupFormTest(SimpleTestCase):
    def setUp(self):
        self.form_instance = forms.JsonStoreLookupPublicForm()

    # FIELDS #
    def test_form_fields_all_present(self):
        fields = [field for field in self.form_instance.fields]
        self.assertIn('jsonstore_name', fields)
        self.assertEqual(len(fields), 1)

    # jsonstore_name
    def test_field_jsonstore_name_field_type(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].__class__.__name__,
            'CharField')

    def test_field_jsonstore_name_label(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].label,
            c.STORES_JSONSTORE_LOOKUP_PUBLIC_FORM_LABEL)

    def test_field_jsonstore_name_max_length(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].max_length,
            c.JSONSTORE_NAME_MAX_LENGTH)

    def test_field_jsonstore_name_max_help_text(self):
        self.assertEqual(
            self.form_instance.fields['jsonstore_name'].help_text,
            c.STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT)
