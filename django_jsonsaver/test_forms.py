from django.test import SimpleTestCase

from . import constants as c
from . import forms


class ContactUsFormTest(SimpleTestCase):
    def setUp(self):
        self.form = forms.ContactUsForm
        self.form_instance = forms.ContactUsForm()

    # FIELDS #
    def test_form_fields_all_present(self):
        fields = [field for field in self.form_instance.fields]
        self.assertIn('first_name', fields)
        self.assertIn('last_name', fields)
        self.assertIn('email', fields)
        self.assertIn('message', fields)
        self.assertIn('captcha', fields)
        self.assertTrue(len(fields), 5)

    # first_name
    def test_field_first_name_field_type(self):
        self.assertEqual(
            self.form_instance.fields['first_name'].__class__.__name__,
            'CharField')

    def test_field_first_name_label(self):
        label = self.form_instance.fields['first_name'].label
        self.assertEqual(label, 'Name')

    def test_field_first_name_max_length(self):
        max_length = self.form_instance.fields['first_name'].max_length
        self.assertEqual(max_length, 128)

    # last_name
    def test_field_last_name_field_type(self):
        self.assertEqual(
            self.form_instance.fields['last_name'].__class__.__name__,
            'CharField')

    def test_field_last_name_widget(self):
        widget = \
            self.form_instance.fields['last_name'].widget.__class__.__name__
        self.assertEqual(widget, 'HiddenInput')

    def test_field_last_name_required(self):
        required = self.form_instance.fields['last_name'].required
        self.assertEqual(required, False)

    # email
    def test_field_email_field_type(self):
        self.assertEqual(
            self.form_instance.fields['email'].__class__.__name__,
            'EmailField')

    # message
    def test_field_message_field_type(self):
        self.assertEqual(
            self.form_instance.fields['message'].__class__.__name__,
            'CharField')

    def test_field_message_widget(self):
        widget = \
            self.form_instance.fields['message'].widget.__class__.__name__
        self.assertEqual(widget, 'Textarea')

    # captcha
    def test_field_captcha_field_type(self):
        self.assertEqual(
            self.form_instance.fields['captcha'].__class__.__name__,
            'CaptchaField')

    def test_field_captcha_label(self):
        label = self.form_instance.fields['captcha'].label
        self.assertEqual(label, 'CAPTCHA')

    def test_field_captcha_help_text(self):
        help_text = self.form_instance.fields['captcha'].help_text
        self.assertEqual(help_text, c.FORM_FIELD_CAPTCHA_HELP_TEXT)
