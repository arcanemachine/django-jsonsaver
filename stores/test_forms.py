from django.core.exceptions import ValidationError
from django.forms import widgets
from django.test import SimpleTestCase, TestCase

from . import forms
from .models import JsonStore
from django_jsonsaver import constants as c, factories as f


class JsonStoreFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = forms.JsonStoreForm
        cls.form_instance = forms.JsonStoreForm()
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = f.JsonStoreFactory(user=cls.test_user)

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

    # VALIDATION #
    def test_validation_jsonstore_is_public_and_not_name(self):
        form_data = {'data': {},
                     'name': '',
                     'is_public': True}
        form = forms.JsonStoreForm(data=form_data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError):
            form.clean()


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
