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

        # public store name cannot be blank
        if is_public and not name:
            raise ValidationError(c.FORM_ERROR_STORE_PUBLIC_NAME_BLANK)

        # store name not allowed
        if name and name in c.FORBIDDEN_STORE_NAMES:
            raise ValidationError(
                f"The name '{name}' cannot be used as a store name.")

        # user has too many stores
        max_store_count = user.profile.get_max_store_count()
        if user.jsonstore_set.count() >= max_store_count:
            raise ValidationError(
                f"You have reached the maximum of {max_store_count} "
                "JSON stores. You cannot create any more stores.")

        # duplicate store name
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

        # store size is too large
        store_data_size = helpers.get_obj_size(store_data)
        if store_data_size > user.profile.get_max_store_data_size():
            raise ValidationError(
                c.FORM_ERROR_STORE_DATA_SIZE_OVER_MAX(user, store_data_size))

        # store size will exceed user's total storage allowance
        if store_data_size + user.profile.get_all_stores_data_size() > \
                user.profile.get_max_all_stores_data_size():
            raise ValidationError(
                c.FORM_ERROR_ALL_STORES_DATA_SIZE_OVER_MAX(
                    user, store_data_size))

        return self.cleaned_data
