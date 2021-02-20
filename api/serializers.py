from rest_framework import serializers

from jsonsaver.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'ref', 'data']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            user = None
        jsonstore = JsonStore.objects.create(user=user, **validated_data)
        return jsonstore


class JsonStoreRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data']
        read_only_fields = ['data']
