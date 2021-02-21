from rest_framework import permissions

from jsonsaver.models import JsonStore


class HasJsonStorePermissionsOrPublicReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        elif type(obj) == JsonStore:
            if obj.is_public:
                return True
            return request.user == obj.user
        # if non-jsonstore object submitted, raise TypeError
        else:
            raise TypeError(
                "This permission can only be used with a JsonStore object.")
