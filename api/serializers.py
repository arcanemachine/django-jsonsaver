from django.utils.text import slugify
from rest_framework import serializers

from django_jsonsaver import constants as c, helpers as h
from stores import invalidators
from stores.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(initial={}, required=False)

    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'data', 'name', 'is_public']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        jsonstore = JsonStore.objects.create(user=user, **validated_data)
        return jsonstore

    def validate_name(self, value):
        return slugify(value)

    def validate(self, data):
        name = slugify(data.get('name', ''))
        jsonstore_data = data.get('data', {})
        is_public = data.get('is_public', False)

        user = self.context['request'].user
        obj = self.instance

        # public jsonstore name cannot be blank
        if invalidators.jsonstore_public_name_cannot_be_blank(name, is_public):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK,
                code='jsonstore_public_name_cannot_be_blank')

        # forbidden jsonstore name not allowed
        if invalidators.jsonstore_forbidden_name_not_allowed(name):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_FORBIDDEN_NAME_NOT_ALLOWED(name),
                code='jsonstore_forbidden_name_not_allowed')

        # user jsonstore count over max
        user_max_jsonstore_count = user.profile.get_max_jsonstore_count()
        if invalidators.jsonstore_user_jsonstore_count_over_max(
                user, user_max_jsonstore_count):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_USER_JSONSTORE_COUNT_OVER_MAX(
                    user, user_max_jsonstore_count),
                code='jsonstore_user_jsonstore_count_over_max')

        stores_with_same_name = JsonStore.objects.filter(name=name)

        # jsonstore_name_duplicate_same_user_create
        if invalidators.jsonstore_name_duplicate_same_user_create(
                name, user, obj, stores_with_same_name):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                code='jsonstore_name_duplicate_same_user_create')

        # jsonstore_name_duplicate_same_user_update
        if invalidators.jsonstore_name_duplicate_same_user_update(
                name, user, obj, stores_with_same_name):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
                code='jsonstore_name_duplicate_same_user_update')

        # jsonstore_public_name_duplicate
        if invalidators.jsonstore_public_name_duplicate(
                name, is_public, user, stores_with_same_name):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE,
                code='jsonstore_public_name_duplicate')

        jsonstore_data_size = h.get_obj_size(jsonstore_data)

        # jsonstore data size over max
        if invalidators.jsonstore_data_size_over_max(
                jsonstore_data, user, jsonstore_data_size):
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='jsonstore_data_size_over_max')

        # jsonstore size will exceed user's total storage allowance
        if invalidators.jsonstore_all_jsonstores_data_size_over_max(
                user, jsonstore_data_size):
            raise serializers.ValidationError(
                c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size),
                code='jsonstore_all_jsonstores_data_size_over_max')

        return data


class JsonStoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data', 'is_public']


class JsonStorePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonStore
        fields = ['data']
        read_only_fields = ['data']
