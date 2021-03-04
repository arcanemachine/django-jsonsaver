from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers
from .permissions import HasJsonStorePermissions
from stores.models import JsonStore


def api_root(request):
    return HttpResponseRedirect(reverse('api_generic:schema'))


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer
    permission_classes = [IsAuthenticated, HasJsonStorePermissions]

    def list(self, request):
        self.queryset = JsonStore.objects.filter(user__id=request.user.id)
        return super().list(request)


class JsonStoreNameDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.JsonStoreNameSerializer
    permission_classes = [HasJsonStorePermissions]

    def get_object(self):
        return get_object_or_404(
            JsonStore,
            name=self.kwargs['jsonstore_name'],
            user__id=self.request.user.id)


class JsonStorePublicDetail(generics.RetrieveAPIView):
    serializer_class = serializers.JsonStorePublicSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            JsonStore, name=self.kwargs['jsonstore_name'], is_public=True)
