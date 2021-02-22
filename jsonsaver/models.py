from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class JsonStore(models.Model):
    user = \
        models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=128, blank=True, null=True,
        help_text="Name will be lowercased and hyphenated for use in URLs.")
    is_public = models.BooleanField(
        help_text="Make this store publicly accessible by name.",
        default=False)

    data = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.id}, "\
            f"user: {self.user.username}, "\
            f"name: {self.name if self.name else 'N/A'}, "\
            f"is_public: {self.is_public}"

    def get_absolute_url(self):
        return reverse('jsonsaver:jsonstore_detail', kwargs={
            'jsonstore_pk': self.pk})

    def save(self, *args, **kwargs):
        if self.name and self.name != slugify(self.name):
            self.name = slugify(self.name)
        super().save(*args, **kwargs)


"""
store = {
  "user": 1,
  "name": "dog-food",
"data": {
  "users": [
    {
      "id": 1,
      "token": "8479437015867",
      "data":
      {
        "username": "billmurray",
        "password": "3F8V%24NtX*9S.9Vi)Kjwid",
        "email": "billmurray@email.com",
        "favorites": ["dogs", "cats", "bears"]
      }
    }
  ]
}
}
"""
