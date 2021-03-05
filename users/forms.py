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
            # email is registered to another user
            self.add_error('email', ValidationError(
                c.USER_FORM_EMAIL_ERROR_DUPLICATE,
                code='email_error_duplicate'))
        return email

    def clean_username(self):
        return self.data['username'].lower()


class UserAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    def clean_username(self):
        return self.data['username'].lower()


class UserActivationEmailResendForm(forms.Form):
    email = forms.EmailField(label="Enter your email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)


class UserUpdateEmailForm(forms.Form):
    email = forms.EmailField(label="Enter your new email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.data['email'].lower()
        users_with_this_email = UserModel.objects.filter(email=email)
        if users_with_this_email.exists():

            # email is user's current email address
            if users_with_this_email.first() == self.user:
                self.add_error('email', ValidationError(
                    c.USER_FORM_EMAIL_ERROR_SAME_EMAIL,
                    code='email_error_same_email'))

            # email is registered to another user
            else:
                self.add_error('email', ValidationError(
                    c.USER_FORM_EMAIL_ERROR_DUPLICATE,
                    code='email_error_duplicate'))

        return email


class UserUsernameRecoverForm(forms.Form):
    email = forms.EmailField(label="Your email address")
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)


class UserPasswordResetForm(PasswordResetForm):
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
