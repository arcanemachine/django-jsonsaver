from rest_framework import permissions

from stores.models import JsonStore


class HasJsonStorePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if type(obj) != JsonStore:
            raise TypeError(
                "This permission can only be used with a JsonStore object.")
        if request.user.is_staff:
            return True
        return request.user == obj.user
