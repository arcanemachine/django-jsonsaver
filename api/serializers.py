from django.utils.text import slugify
from rest_framework import serializers

from jsonsaver.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()

    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'is_public', 'name', 'data']
        read_only_fields = ['user']

    def validate(self, data):
        name = data.get('name', None)
        is_public = data.get('is_public', False)

        user = self.context['request'].user
        obj = self.instance

        if is_public and not name:
            raise serializers.ValidationError(
                "Publicly accessible stores must be given a name.")

        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))

        if is_public:
            different_user_public_stores_with_same_name = \
                stores_with_same_name.exclude(user=user).filter(is_public=True)
            if different_user_public_stores_with_same_name.exists():
                raise serializers.ValidationError(
                    "This publicly accessible store name is already in use.")
        if obj:
            other_user_stores_with_same_name = \
                stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if other_user_stores_with_same_name.exists():
                raise serializers.ValidationError(
                    "You cannot have multiple stores with the same name.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        jsonstore = JsonStore.objects.create(user=user, **validated_data)
        return jsonstore


class JsonStoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data', 'is_public']
        read_only_fields = ['data', 'is_public']
