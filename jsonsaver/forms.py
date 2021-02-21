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
        super().__init__(*args, **kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        is_public = self.data.get('is_public')
        if name:
            stores_with_same_name = \
                JsonStore.objects.filter(name=slugify(name))
            public_stores_with_same_name = \
                stores_with_same_name.filter(is_public=True)
            breakpoint()
            if is_public and public_stores_with_same_name.count() \
                    and public_stores_with_same_name.first().user != self.user:
                raise ValidationError(
                    "There is already a publicly accessible store with this "
                    "name. Please choose another name if you want this store "
                    "to be publicly accessible.")
            elif stores_with_same_name.filter(user=self.user).exists() \
                    and stores_with_same_name.first().pk == self.cleaned:
                raise ValidationError(
                    "You cannot have multiple stores with the same name.")
        elif not name and is_public:
            raise ValidationError(
                "Publicly accessible stores must be given a name.")
        return self.cleaned_data
