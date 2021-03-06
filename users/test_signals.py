from django.test import TestCase
from rest_framework.authtoken.models import Token

from .models import Profile
from django_jsonsaver import factories as f


class UserSignalsTest(TestCase):
    def test_new_user_creation_triggers_api_token_creation(self):
        old_token_count = Token.objects.count()
        f.UserFactory()
        new_token_count = Token.objects.count()
        self.assertEqual(new_token_count, old_token_count + 1)

    def test_new_user_creation_triggers_user_profile_creation(self):
        old_profile_count = Profile.objects.count()
        f.UserFactory()
        new_profile_count = Profile.objects.count()
        self.assertTrue(new_profile_count == old_profile_count + 1)