from django.utils.text import slugify
from rest_framework import serializers

from django_jsonsaver import constants as c
from django_jsonsaver import helpers
from jsonsaver.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(initial={})

    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'is_public', 'name', 'data']
        read_only_fields = ['user']

    def validate(self, data):
        name = data.get('name', None)
        store_data = data.get('data', {})
        is_public = data.get('is_public', False)

        user = self.context['request'].user
        obj = self.instance

        if len(store_data) and helpers.get_obj_size(store_data) > \
                c.JSONSTORE_DATA_SIZE_MAX:
            raise serializers.ValidationError(
                c.FORM_ERROR_STORE_DATA_SIZE_OVER_MAX +
                " The size of your store's JSON data "
                f"{round(helpers.get_obj_size(store_data) / 1024, 2)} KB.")

        if is_public and not name:
            raise serializers.ValidationError(
                c.FORM_ERROR_STORE_PUBLIC_NAME_BLANK)

        stores_with_same_name = JsonStore.objects.filter(name=slugify(name))

        if is_public:
            different_user_public_stores_with_same_name = \
                stores_with_same_name.exclude(user=user).filter(is_public=True)
            if different_user_public_stores_with_same_name.exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_STORE_PUBLIC_NAME_DUPLICATE)
        if obj:
            same_user_stores_with_same_name = \
                stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if name and same_user_stores_with_same_name.exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_STORE_NAME_DUPLICATE)
        else:
            if name and stores_with_same_name.filter(user=user).exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_STORE_NAME_DUPLICATE)
        return data

    def create(self, validated_data):
        # if user has too many stores, do not continue
        user = self.context['request'].user
        if user.jsonstore_set.count() >= user.profile.jsonstore_count_max:
            raise serializers.ValidationError(
                "You have reached the maximum of "
                f"{user.profile.jsonstore_count_max} JSON stores. You cannot "
                "create any more stores.")
        user = self.context['request'].user
        jsonstore = JsonStore.objects.create(user=user, **validated_data)
        return jsonstore


class JsonStoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data', 'is_public']


class JsonStorePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data']
        read_only_fields = ['data']
