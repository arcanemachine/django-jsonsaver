from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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
        name = self.cleaned_data.get('name')
        jsonstore_data = self.cleaned_data.get('data')
        is_public = self.data.get('is_public')

        user = self.user
        obj = self.obj

        # public store name cannot be blank
        if is_public and not name:
            self.add_error('name', ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK,
                code='public_jsonstore_name_cannot_be_blank'))

        # forbidden store name not allowed
        if name and name in c.FORBIDDEN_JSONSTORE_NAMES:
            self.add_error('name', ValidationError(
                "The name '%(name)s' cannot be used as a store name.",
                code='forbidden_jsonstore_name_not_allowed',
                params={'name': name}))

        # user has too many stores
        max_jsonstore_count = user.profile.get_max_jsonstore_count()
        if user.jsonstore_set.count() >= max_jsonstore_count:
            self.add_error(None, ValidationError(
                "You have reached the maximum of %(max_jsonstore_count)s "
                "JSON stores. You cannot create any more stores.",
                code='user_has_too_many_jsonstores',
                params={'max_jsonstore_count': max_jsonstore_count}))

        # store name duplicate
        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))
        if is_public:
            other_user_public_jsonstores_with_same_name = \
                stores_with_same_name.exclude(user=user).filter(is_public=True)
            if other_user_public_jsonstores_with_same_name.exists():
                # store public name duplicate
                self.add_error('name', ValidationError(
                    c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE,
                    code='jsonstore_public_name_duplicate_other_user'))
        if obj:
            same_user_jsonstores_with_same_name = \
                stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if name and same_user_jsonstores_with_same_name.exists():
                # store name duplicate
                self.add_error('name', ValidationError(
                    c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                    code='jsonstore_name_duplicate_same_user'))
        else:
            if name and stores_with_same_name.filter(user=user).exists():
                # store name duplicate
                self.add_error('name', ValidationError(
                    c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                    code='jsonstore_name_duplicate_same_user'))

        # store data size over max
        jsonstore_data_size = h.get_obj_size(jsonstore_data)
        if jsonstore_data_size > user.profile.get_max_jsonstore_data_size():
            self.add_error('data', ValidationError(
                c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='jsonstore_data_size_over_max'))

        # store size will exceed user's total storage allowance
        if jsonstore_data_size + user.profile.get_all_jsonstores_data_size() >\
                user.profile.get_max_all_jsonstores_data_size():
            self.add_error('data', ValidationError(
                c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='all_jsonstores_data_size_over_max'))

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
