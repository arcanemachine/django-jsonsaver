from django.forms import widgets
from django.test import SimpleTestCase

from django_jsonsaver import constants as c
from . import forms


class JsonStoreLookupFormTest(SimpleTestCase):
    def setUp(self):
        self.form = forms.JsonStoreLookupForm
        self.form_instance = forms.JsonStoreLookupForm()

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
        self.form = forms.JsonStoreLookupPublicForm
        self.form_instance = forms.JsonStoreLookupPublicForm()

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
