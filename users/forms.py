from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from django_jsonsaver import constants as c

UserModel = get_user_model()


class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaField(help_text=c.FORMS_CAPTCHA_FIELD_HELP_TEXT)

    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        if UserModel.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError("This email address is taken.")
        return self.cleaned_data['email'].lower()

    def clean_username(self):
        return self.cleaned_data['username'].lower()

class UserAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(help_text=c.FORMS_CAPTCHA_FIELD_HELP_TEXT)
