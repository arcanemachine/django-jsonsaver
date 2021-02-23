from django import forms
from captcha.fields import CaptchaField

from . import constants as c


class JsonStorePublicSearchForm(forms.Form):
    jsonstore_public_name = \
        forms.CharField(label="Find a public JSON store", max_length=128,
            help_text="Your query will be converted to a URL-friendly format. "
            "e.g. 'My Public STORE!' &rarr; 'my-public-store'")
    # captcha = CaptchaField(help_text=c.FORMS_CAPTCHA_FIELD_HELP_TEXT)
