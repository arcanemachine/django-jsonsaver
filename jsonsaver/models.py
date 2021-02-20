from django.conf import settings
from django.db import models
from rest_framework.authtoken.models import Token


class JsonStore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    ref = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_public = models.BooleanField(default=False)

    data = models.JSONField(default=dict, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"id: {self.id}, "\
            f"user: {self.user.username}, "\
            f"ref: {self.ref if self.ref else 'N/A'}"


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
