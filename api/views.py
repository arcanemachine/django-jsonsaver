from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser

from . import serializers
from .permissions import HasJsonStorePermissionsOrPublicReadOnly
from jsonsaver.models import JsonStore


def api_root(request):
    return HttpResponseRedirect(reverse('project_root'))


def jsonstore_detail_name_root(request):
    return JsonResponse(
        {"message": "Stores can be requested by name via GET: " +
            reverse('api:name_root') + '[store_name]/'})


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer

    def list(self, request):
        self.queryset = JsonStore.objects.filter(user=request.user)
        return super().list(request)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or obj.user == user:
            return obj
        raise PermissionDenied


class JsonStoreListAll(generics.ListAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer
    permission_classes = [IsAdminUser]


class JsonStoreDetailName(generics.RetrieveAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreNameSerializer
    permission_classes = [HasJsonStorePermissionsOrPublicReadOnly]

    def get_object(self):
        qs = JsonStore.objects.filter(name=self.kwargs['name'])
        public_qs = qs.filter(is_public=True)
        if public_qs:
            return public_qs.first()
        elif self.request.user:
            user_qs = qs.filter(user=self.request.user)
            if user_qs.exists():
                return user_qs.first()
        raise NotFound
