from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import JsonStore


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
        is_public = self.data.get('is_public')

        user = self.user
        obj = self.obj

        if is_public and not name:
            raise ValidationError(
                    "Publicly accessible stores must be given a name.")

        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))

        if is_public:
            different_user_public_stores_with_same_name = \
                stores_with_same_name.exclude(user=user).filter(is_public=True)
            if different_user_public_stores_with_same_name.exists():
                raise ValidationError(
                    "This publicly-accessible store name is already in use.")
        if obj:
            same_user_stores_with_same_name = \
                stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if name and same_user_stores_with_same_name.exists():
                raise ValidationError(
                    "You cannot have multiple stores with the same name.")
        else:
            if name and stores_with_same_name.filter(user=user).exists():
                raise ValidationError(
                    "You cannot have multiple stores with the same name.")

        return self.cleaned_data
