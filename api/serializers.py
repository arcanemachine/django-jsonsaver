from rest_framework import serializers

from jsonsaver.models import JsonItem


class JsonItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonItem
        fields = ['id', 'message']
