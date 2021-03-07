from django.test import TestCase

from .models import Profile
from django_jsonsaver import factories as f


class UserSignalsTest(TestCase):
    def test_new_user_creation_triggers_user_profile_creation(self):
        old_profile_count = Profile.objects.count()
        f.UserFactory()
        new_profile_count = Profile.objects.count()
        self.assertTrue(new_profile_count == old_profile_count + 1)
