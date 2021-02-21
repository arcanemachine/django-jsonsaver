from django.utils.text import slugify
from rest_framework import serializers

from jsonsaver.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'is_public', 'name', 'data']
        read_only_fields = ['user']

    def validate(self, data):
        if data.get('is_public') == True and not data['name']:
            raise serializers.ValidationError(
                "Publicly accessible stores must be given a name.")
        if data.get('is_public') == True and \
                JsonStore.objects.filter(name=slugify(data['name'])).exists():
            raise serializers.ValidationError(
                "There is already a publicly accessible store with this name.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        jsonstore = JsonStore.objects.create(user=user, **validated_data)
        return jsonstore


class JsonStoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data']
        read_only_fields = ['data']
