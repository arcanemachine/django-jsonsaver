from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from . import serializers
from .permissions import HasJsonStorePermissions
from jsonsaver.models import JsonStore


def api_root(request):
    return JsonResponse({
        "message": "Visit jsonSaver.com/api/ to learn how our API works."})


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer
    permission_classes = [HasJsonStorePermissions]

    def list(self, request):
        self.queryset = \
            JsonStore.objects.filter(user__id=request.user.id)
        return super().list(request)


class JsonStoreListAll(generics.ListAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer
    permission_classes = [IsAdminUser]


class JsonStoreDetailName(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.JsonStoreNameSerializer
    permission_classes = [HasJsonStorePermissions]

    def get_object(self):
        return get_object_or_404(
            JsonStore,
            name=self.kwargs['jsonstore_name'],
            user__id=self.request.user.id)


class JsonStoreDetailPublic(generics.RetrieveAPIView):
    serializer_class = serializers.JsonStorePublicSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            JsonStore, name=self.kwargs['jsonstore_name'], is_public=True)
