from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token

from django_jsonsaver import constants as c, helpers as h, server_config as sc

UserModel = get_user_model()


class Profile(models.Model):
    def get_activation_code():
        return Token.generate_key()

    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    activation_code = models.CharField(
        max_length=128, default=get_activation_code, null=True)
    wants_email = models.EmailField(null=True)
    is_public = models.BooleanField(
        verbose_name=c.PROFILE_MODEL_IS_PUBLIC_VERBOSE_NAME,
        help_text=c.PROFILE_MODEL_IS_PUBLIC_HELP_TEXT,
        default=False)
    account_tier = models.CharField(max_length=128, default='free')

    def get_absolute_url(self):
        return self.user.get_absolute_url()

    def get_all_jsonstores_data_size(self):
        result = 0
        for store in self.user.jsonstore_set.all():
            result += h.get_obj_size(store.data)
        return result

    def get_all_jsonstores_data_size_in_kb(self):
        return round(self.get_all_jsonstores_data_size() / 1024, 2)

    def get_max_jsonstore_count(self):
        if self.account_tier == 'free':
            return sc.MAX_JSONSTORE_COUNT_USER_FREE

    def get_max_jsonstore_data_size(self):
        if self.account_tier == 'free':
            return sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE

    def get_max_jsonstore_data_size_in_kb(self):
        if self.account_tier == 'free':
            return h.bytes_to_kb(sc.MAX_JSONSTORE_DATA_SIZE_USER_FREE)

    def get_max_jsonstore_all_jsonstores_data_size(self):
        if self.account_tier == 'free':
            return sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE

    def get_max_jsonstore_all_jsonstores_data_size_in_kb(self):
        if self.account_tier == 'free':
            return h.bytes_to_kb(
                sc.MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE)
