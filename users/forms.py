from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import \
    UserCreationForm, AuthenticationForm, PasswordResetForm
from django.core.exceptions import ValidationError

from django_jsonsaver import constants as c

UserModel = get_user_model()


class NewUserCreationForm(UserCreationForm):
    # honeypot field - name
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.EmailField()
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.data['email'].lower()
        if UserModel.objects.filter(email=email).exists():
            self.add_error('email', ValidationError(
                c.USER_FORM_EMAIL_ERROR_DUPLICATE,
                code='email_error_duplicate'))
        return email

    def clean_username(self):
        return self.data['username'].lower()


class UserAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    def clean_username(self):
        return self.data['username'].lower()


class UserActivationEmailResendForm(forms.Form):
    email = forms.EmailField(label="Your email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)


class UserUpdateEmailForm(forms.Form):
    email = forms.EmailField(label="Enter your email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    def clean(self):
        # do not allow duplicate email addresses
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            self.add_error('email', ValidationError(
                c.USER_FORM_EMAIL_ERROR_DUPLICATE,
                code='email_error_duplicate'))
        return self.cleaned_data


class UserUsernameRecoverForm(forms.Form):
    email = forms.EmailField(label="Your email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)


class UserPasswordResetForm(PasswordResetForm):
    captcha = CaptchaField(help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
