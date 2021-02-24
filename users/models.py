from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=128, null=True)
    is_public = models.BooleanField(
        "Make this profile public",
        help_text="If this setting is active, users can look up this profile "\
            "based on your username and view all your public stores.",
        default=False)

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = Token.generate_key()
        super().save(*args, **kwargs)
