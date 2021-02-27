from captcha.fields import CaptchaField
from django import forms

from . import constants as c


class ContactUsForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=128)
    # honeypot field
    last_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.widgets.Textarea)
    captcha = CaptchaField(
        label="CAPTCHA", help_text=c.FORM_FIELD_CAPTCHA_HELP_TEXT)
