from captcha.fields import CaptchaField
from django import forms

from . import constants as c


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.widgets.Textarea)
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
