from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import JsonStore
from django_jsonsaver import constants as c
from django_jsonsaver import helpers


class JsonStoreLookupForm(forms.Form):
    name = forms.CharField(
        label="Find a public JSON store", max_length=128,
        help_text="Your query will be converted to a URL-friendly format. "
        "e.g. 'My Public STORE!' &rarr; 'my-public-store'")


class JsonStoreLookupPublicForm(forms.Form):
    name = forms.CharField(
        label="Find a public JSON store", max_length=128,
        help_text="Your query will be converted to a URL-friendly format. "
        "e.g. 'My Public STORE!' &rarr; 'my-public-store'")


class JsonStoreForm(forms.ModelForm):
    class Meta:
        model = JsonStore
        fields = ['data', 'name', 'is_public']
        widgets = {'data': forms.Textarea}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.obj = kwargs.pop('obj', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        store_data = self.cleaned_data.get('data')
        is_public = self.data.get('is_public')

        user = self.user
        obj = self.obj

        if name and name in c.FORBIDDEN_STORE_NAMES:
            raise ValidationError(
                f"The name '{name}' cannot be used as a store name.")

        if len(store_data):
            if helpers.get_obj_size(store_data) > c.JSONSTORE_DATA_MAX_SIZE:
                raise ValidationError(
                    c.FORM_ERROR_STORE_DATA_OVER_MAX_SIZE +
                    " The size of your store's JSON data "
                    f"{round(helpers.get_obj_size(store_data) / 1024, 2)} KB.")

        if is_public and not name:
            raise ValidationError(c.FORM_ERROR_STORE_PUBLIC_NAME_BLANK)

        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))

        if is_public:
            different_user_public_stores_with_same_name = \
                stores_with_same_name.exclude(user=user).filter(is_public=True)
            if different_user_public_stores_with_same_name.exists():
                raise ValidationError(c.FORM_ERROR_STORE_PUBLIC_NAME_DUPLICATE)
        if obj:
            same_user_stores_with_same_name = \
                stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if name and same_user_stores_with_same_name.exists():
                raise ValidationError(c.FORM_ERROR_STORE_NAME_DUPLICATE)
        else:
            if name and stores_with_same_name.filter(user=user).exists():
                raise ValidationError(c.FORM_ERROR_STORE_NAME_DUPLICATE)

        return self.cleaned_data
