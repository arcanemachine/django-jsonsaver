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
        current_user = self.context['request'].user

        if is_public and not name:
            raise serializers.ValidationError(
                "Publicly accessible stores must be given a name.")

        stores_with_same_name = JsonStore.objects.filter(
            name=slugify(name)).order_by('-updated_at')
        public_stores_with_same_name = \
            stores_with_same_name.filter(is_public=True)
        user_stores_with_same_name = \
            stores_with_same_name.filter(user=current_user)

        if is_public and public_stores_with_same_name.count() \
                and not hasattr(self.instance, 'user') \
                or is_public and public_stores_with_same_name.count() \
                and public_stores_with_same_name.last().user != current_user:
            raise serializers.ValidationError(
                "There is already a publicly accessible store with this name.")
        elif user_stores_with_same_name.count() \
                and not hasattr(self.instance, 'pk') \
                or user_stores_with_same_name.count() \
                and user_stores_with_same_name.last().pk != self.instance.pk:
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
