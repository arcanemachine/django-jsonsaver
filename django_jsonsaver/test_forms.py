from django.test import TestCase

from . import constants as c
from . import forms


class ContactUsFormTest(TestCase):
    def setUp(self):
        self.test_form = forms.ContactUsForm
        self.test_form_instance = forms.ContactUsForm()

    # ATTRIBUTES #
    def test_form_class_name(self):
        self.assertEqual(self.test_form.__name__, 'ContactUsForm')

    def test_form_parent_class_name(self):
        self.assertEqual(self.test_form.__bases__[-1].__name__, 'Form')

    # FIELDS #
    def test_form_fields_all_present(self):
        fields = [field for field in self.test_form_instance.fields]
        self.assertIn('first_name', fields)
        self.assertIn('last_name', fields)
        self.assertIn('email', fields)
        self.assertIn('message', fields)
        self.assertIn('captcha', fields)
        self.assertTrue(len(fields), 5)

    # first_name
    def test_field_first_name_field_type(self):
        self.assertEqual(
            self.test_form_instance.fields['first_name'].__class__.__name__,
            'CharField')

    def test_field_first_name_label(self):
        label = self.test_form_instance.fields['first_name'].label
        self.assertEqual(label, 'Name')

    def test_field_first_name_max_length(self):
        max_length = self.test_form_instance.fields['first_name'].max_length
        self.assertEqual(max_length, 128)

    # last_name
    def test_field_last_name_field_type(self):
        self.assertEqual(
            self.test_form_instance.fields['last_name'].__class__.__name__,
            'CharField')

    def test_field_last_name_widget(self):
        widget = self.test_form_instance.fields['last_name'] \
            .widget.__class__.__name__
        self.assertEqual(widget, 'HiddenInput')

    def test_field_last_name_required(self):
        required = self.test_form_instance.fields['last_name'].required
        self.assertEqual(required, False)

    # email
    def test_field_email_field_type(self):
        self.assertEqual(
            self.test_form_instance.fields['email'].__class__.__name__,
            'EmailField')

    # message
    def test_field_message_field_type(self):
        self.assertEqual(
            self.test_form_instance.fields['message'].__class__.__name__,
            'CharField')

    def test_field_message_widget(self):
        widget = \
            self.test_form_instance.fields['message'].widget.__class__.__name__
        self.assertEqual(widget, 'Textarea')

    # captcha
    def test_field_captcha_field_type(self):
        self.assertEqual(
            self.test_form_instance.fields['captcha'].__class__.__name__,
            'CaptchaField')

    def test_field_captcha_label(self):
        label = self.test_form_instance.fields['captcha'].label
        self.assertEqual(label, 'CAPTCHA')

    def test_field_captcha_help_text(self):
        help_text = self.test_form_instance.fields['captcha'].help_text
        self.assertEqual(help_text, c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    # FUNCTIONAL #
    def test_functional_valid_form_submitted(self):
        form_data = {
            'first_name': c.TEST_USER_FULL_NAME,
            'email': c.TEST_USER_EMAIL,
            'message': c.TEST_MESSAGE,
            'captcha_0': 'test',
            'captcha_1': 'PASSED',
        }
        form = self.test_form(data=form_data)
        self.assertTrue(form.is_valid())
