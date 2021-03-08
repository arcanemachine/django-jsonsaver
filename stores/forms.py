from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from . import invalidators
from .models import JsonStore
from django_jsonsaver import constants as c, helpers as h


class JsonStoreForm(forms.ModelForm):
    class Meta:
        model = JsonStore
        fields = ['data', 'name', 'is_public']
        widgets = {'data': forms.Textarea}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.obj = kwargs.pop('obj', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        return slugify(self.data['name'])

    def clean(self):
        jsonstore_data = self.cleaned_data.get('data')
        name = self.cleaned_data.get('name')
        is_public = self.data.get('is_public')

        user = self.user
        obj = self.obj

        # name cannot be numbers only
        if invalidators.jsonstore_name_cannot_be_numbers_only(name):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_NAME_CANNOT_BE_NUMBERS_ONLY,
                code='jsonstore_name_cannot_be_numbers_only'))

        # public jsonstore name cannot be blank
        if invalidators.jsonstore_public_name_cannot_be_blank(name, is_public):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK,
                code='jsonstore_public_name_cannot_be_blank'))

        # forbidden jsonstore name not allowed
        if invalidators.jsonstore_forbidden_name_not_allowed(name):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_FORBIDDEN_NAME_NOT_ALLOWED(name),
                code='jsonstore_forbidden_name_not_allowed'))

        # user jsonstore count over max
        user_max_jsonstore_count = user.profile.get_max_jsonstore_count()
        if invalidators.jsonstore_user_jsonstore_count_over_max(
                user, user_max_jsonstore_count):
            self.add_error(None, ValidationError(
                c.FORM_ERROR_JSONSTORE_USER_JSONSTORE_COUNT_OVER_MAX(
                    user, user_max_jsonstore_count),
                code='jsonstore_user_jsonstore_count_over_max'))

        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))

        # jsonstore_name_duplicate_same_user_create
        if invalidators.jsonstore_name_duplicate_same_user_create(
                name, user, obj, stores_with_same_name):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                code='jsonstore_name_duplicate_same_user_create'))

        # jsonstore_name_duplicate_same_user_update
        if invalidators.jsonstore_name_duplicate_same_user_update(
                name, user, obj, stores_with_same_name):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                code='jsonstore_name_duplicate_same_user_update'))

        # jsonstore_public_name_duplicate
        if invalidators.jsonstore_public_name_duplicate(
                name, is_public, user, stores_with_same_name):
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE,
                code='jsonstore_public_name_duplicate'))

        jsonstore_data_size = h.get_obj_size(jsonstore_data)

        # jsonstore data size over max
        if invalidators.jsonstore_data_size_over_max(
                jsonstore_data, user, jsonstore_data_size):
            self.add_error('data', ValidationError(
                c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='jsonstore_data_size_over_max'))

        # jsonstore size will exceed user's total storage allowance
        if invalidators.jsonstore_all_jsonstores_data_size_over_max(
                user, jsonstore_data_size):
            self.add_error('data', ValidationError(
                c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='jsonstore_all_jsonstores_data_size_over_max'))

        return self.cleaned_data


class JsonStoreLookupForm(forms.Form):
    jsonstore_name = forms.CharField(
        label=c.STORES_JSONSTORE_LOOKUP_FORM_LABEL,
        max_length=c.JSONSTORE_NAME_MAX_LENGTH,
        help_text=c.STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT)


class JsonStorePublicLookupForm(forms.Form):
    jsonstore_name = forms.CharField(
        label=c.STORES_JSONSTORE_PUBLIC_LOOKUP_FORM_LABEL,
        max_length=c.JSONSTORE_NAME_MAX_LENGTH,
        help_text=c.STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT)
