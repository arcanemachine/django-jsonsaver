from django.conf import settings
from django.db import models


class JsonStore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ref = models.CharField(max_length=255, blank=True, null=True)
    store_token = models.CharField(max_length=255, blank=True, null=True)
    access_tokens = models.JSONField(default=dict, blank=False, null=True)

    data = models.JSONField(default=dict, blank=False, null=True)


"""
store = {
  "user": 1,
  "store_token": "75948753497637690",
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
