from django.contrib.auth.mixins import UserPassesTestMixin


class UserHasJsonStorePermissionsMixin(UserPassesTestMixin):
    def test_func(self, obj=None):
        if self.request.user.is_staff:
            return True
        else:
            obj = self.get_object()
            if obj.user == self.request.user:
                return True
        return False
