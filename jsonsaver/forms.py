from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import JsonStore


class JsonStoreForm(forms.ModelForm):
    class Meta:
        model = JsonStore
        fields = ['data', 'name', 'is_public']
        widgets = {'data': forms.Textarea}

    def clean(self):
        name = self.cleaned_data['name']
        if self.data.get('is_public') \
                and JsonStore.objects.filter(name=slugify(name)).exists():
            raise ValidationError(
                "There is already a publicly accessible store with this name. "
                "Please choose another name if you want this store to be "
                "publicly accessible.")
        return self.cleaned_data
