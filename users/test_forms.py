from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.test import TestCase

from . import forms
from django_jsonsaver import constants as c, factories as f


class NewUserCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_form = forms.NewUserCreationForm
        cls.test_form_instance = forms.NewUserCreationForm()

    def setUp(self):
        self.test_form_data = {'username': c.TEST_USER_USERNAME,
                               'email': c.TEST_USER_EMAIL,
                               'name': '',
                               'password1': c.TEST_USER_PASSWORD,
                               'password2': c.TEST_USER_PASSWORD,
                               'captcha_0': 'test',
                               'captcha_1': 'PASSED'}

    # ATTRIBUTES #
    def test_form_class_name(self):
        self.assertEqual(self.test_form.__name__, 'NewUserCreationForm')

    def test_form_parent_class_name(self):
        self.assertEqual(
            self.test_form.__bases__[-1].__name__, 'UserCreationForm')

    # FIELDS #

    # name
    def test_field_name_field_type(self):
        field_type = \
            self.test_form_instance.fields['name'].__class__.__name__
        self.assertEqual(field_type, 'CharField')

    def test_field_name_widget(self):
        widget = self.test_form_instance.fields['name'] \
            .widget.__class__.__name__
        self.assertEqual(widget, 'HiddenInput')

    def test_field_name_required(self):
        required = self.test_form_instance.fields['name'].required
        self.assertEqual(required, False)

    # email
    def test_field_email_field_type(self):
        field_type = self.test_form_instance.fields['email'].__class__.__name__
        self.assertEqual(field_type, 'EmailField')

    # captcha
    def test_field_captcha_field_type(self):
        field_type = \
            self.test_form_instance.fields['captcha'].__class__.__name__
        self.assertEqual(field_type, 'CaptchaField')

    def test_field_captcha_label(self):
        label = self.test_form_instance.fields['captcha'].label
        self.assertEqual(label, 'CAPTCHA')

    def test_field_captcha_help_text(self):
        help_text = self.test_form_instance.fields['captcha'].help_text
        self.assertEqual(help_text, c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    # META #
    def test_meta_model_name(self):
        self.assertEqual(self.test_form.Meta.model.__name__, 'User')

    def test_meta_fields(self):
        self.assertEqual(
            self.test_form.Meta.fields,
            UserCreationForm.Meta.fields + ('email',))

    # METHODS #

    # clean_email()
    def test_clean_email(self):
        form = self.test_form(self.test_form_data)
        self.assertEqual(form.clean_email(), self.test_form_data['email'])
        self.assertTrue(form.is_valid())

    def test_clean_email_returns_lowercase_email(self):
        uppercase_email = self.test_form_data['email'].upper()
        self.test_form_data['email'] = uppercase_email
        form = self.test_form(self.test_form_data)
        self.assertEqual(form.clean_email(), uppercase_email.lower())
        self.assertTrue(form.is_valid())

    def test_clean_email_adds_error_on_duplicate_email(self):
        self.test_user = f.UserFactory(email=c.TEST_USER_EMAIL)
        form = self.test_form(self.test_form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('email', 'email_error_duplicate'))

    # clean_username()
    def test_clean_username_returns_lowercase_username(self):
        uppercase_username = self.test_form_data['username'].upper()
        self.test_form_data['username'] = uppercase_username
        form = self.test_form(self.test_form_data)
        self.assertEqual(form.clean_username(), uppercase_username.lower())
        self.assertTrue(form.is_valid())
