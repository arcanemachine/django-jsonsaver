from rest_framework import generics, viewsets

from . import serializers
from jsonsaver.models import JsonStore


class JsonStoreList(generics.ListAPIView):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer


class JsonStoreViewSet(viewsets.ModelViewSet):
    queryset = JsonStore.objects.all()
    serializer_class = serializers.JsonStoreSerializer
