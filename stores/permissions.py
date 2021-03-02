from django.contrib.auth.mixins import UserPassesTestMixin

from .models import JsonStore


class UserHasJsonStorePermissionsMixin(UserPassesTestMixin):
    def test_func(self, obj=None):
        obj = self.get_object()
        if not isinstance(obj, JsonStore):
            raise TypeError(
                "This permission can only be used with a JsonStore object.")
        if self.request.user.is_staff:
            return True
        if obj.user == self.request.user:
            return True
        return False
