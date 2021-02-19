from rest_framework import generics, viewsets

from . import serializers
from jsonsaver.models import JsonItem


class JsonItemList(generics.ListAPIView):
    queryset = JsonItem.objects.all()
    serializer_class = serializers.JsonItemSerializer


class JsonItemViewSet(viewsets.ModelViewSet):
    queryset = JsonItem.objects.all()
    serializer_class = serializers.JsonItemSerializer
