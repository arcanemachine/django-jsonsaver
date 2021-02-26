from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from rest_framework.authtoken.models import Token

from django_jsonsaver import helpers
from django_jsonsaver import server_config as sc

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

    account_tier = models.CharField(max_length=128, default='free')
    max_user_store_count = \
        models.IntegerField(default=sc.MAX_USER_STORE_COUNT_FREE)
    max_user_store_data_size = \
        models.IntegerField(default=sc.MAX_USER_STORE_DATA_SIZE_FREE)
    max_user_all_stores_data_size = \
        models.IntegerField(default=sc.MAX_USER_ALL_STORES_DATA_SIZE_FREE)

    def get_all_stores_data_size(self):
        result = 0
        for store in self.user.jsonstore_set.all():
            result += helpers.get_obj_size(store.data)
        return result

    def get_all_stores_data_size_in_kb(self):
        return round(self.get_all_stores_data_size() / 1024, 2)

    def get_max_user_all_stores_data_size_in_kb(self):
        return int(self.max_user_all_stores_data_size / 1024)

    def get_absolute_url(self):
        return reverse('users:user_detail_me')
