from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=128, null=True)
    is_public = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = Token.generate_key()
        super().save(*args, **kwargs)
