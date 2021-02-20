from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class JsonStore(models.Model):
    user = \
        models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=128,
        help_text="Note: Name will be converted to lowercase and hyphenated")
    is_public = models.BooleanField(
        "Make this store publicly accessible using the name as a lookup value",
        default=False)

    data = models.JSONField(default=dict, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"id: {self.id}, "\
            f"user: {self.user.username}, "\
            f"name: {self.name if self.name else 'N/A'}"

    def get_absolute_url(self):
        return reverse('users:user_detail')

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = str(self.pk)
        if self.name and self.name != slugify(self.name):
            self.name = slugify(self.name)
        super().save(*args, **kwargs)


"""
store = {
  "user": 1,
  "token": "75948753497637690",
  "ref": "dog-food",
  "access_tokens": {
    "1": {
      "token": "473898275986589",
      "perms": ["read", "write"],
      "expiry_date": null
    }
  },
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
