from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from rest_framework.authtoken.models import Token

from django_jsonsaver.constants import JSONSTORE_COUNT_MAX_FREE

UserModel = get_user_model()


class Profile(models.Model):

    def get_activation_code():
        return {Token.generate_key(): None}

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    activation_code = models.JSONField(default=get_activation_code, null=True)
    wants_email = models.EmailField(null=True)
    is_public = models.BooleanField(
        "Make this profile public",
        help_text="If this setting is active, users can look up this profile "
        "based on your username and view all your public stores.",
        default=False)
    jsonstore_count_max = models.IntegerField(default=JSONSTORE_COUNT_MAX_FREE)

    def get_absolute_url(self):
        return reverse('users:user_detail_me')
