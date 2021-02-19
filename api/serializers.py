from rest_framework import serializers

from jsonsaver.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['id', 'message']
