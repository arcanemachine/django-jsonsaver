from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound

from . import serializers
from jsonsaver.models import JsonStore


def api_root(request):
    return HttpResponseRedirect(reverse('project_root'))


def ref_root(request):
    return HttpResponseRedirect(reverse('project_root'))


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer

    def list(self, request):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().list(request)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff or not obj.user or obj.user == user:
            return obj
        raise PermissionDenied


class JsonStoreRefDetail(generics.RetrieveAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreRefSerializer

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            raise NotFound
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return JsonStore.objects.filter(ref=self.kwargs['ref']).first()
