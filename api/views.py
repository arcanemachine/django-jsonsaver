from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAdminUser

from . import serializers
from jsonsaver.models import JsonStore


def api_root(request):
    return HttpResponseRedirect(reverse('project_root'))


def name_root(request):
    # return HttpResponseRedirect(reverse('project_root'))
    return JsonResponse(
        {"message": "Stores can be requested by name via GET: " +
            reverse('api:name_root') + '[store_name]/'})


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer

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


class JsonStoreNameDetail(generics.RetrieveAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreNameSerializer
    permission_classes = [IsAdminUser]

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            raise NotFound
        elif not obj.is_public and request.user != obj.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return JsonStore.objects.filter(
            name=self.kwargs['name'],
            is_public=True
        ).first()
