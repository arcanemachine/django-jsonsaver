from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from django_jsonsaver import constants as c

UserModel = get_user_model()


class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
    # address = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = UserModel
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        if UserModel.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError("This email address is already in use.")
        return self.cleaned_data['email'].lower()

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    # def clean(self):
    #     if self.cleaned_data.get('address', ''):
    #         return False
    #     return super().clean(self)


class UserAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
