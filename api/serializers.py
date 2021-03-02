from django.utils.text import slugify
from rest_framework import serializers

from django_jsonsaver import constants as c, helpers as h
from stores.models import JsonStore


class JsonStoreSerializer(serializers.ModelSerializer):
    data = serializers.JSONField(initial={})

    class Meta:
        model = JsonStore
        fields = ['id', 'user', 'is_public', 'name', 'data']
        read_only_fields = ['user']

    def validate_name(self, value):
        return slugify(value)

    def validate(self, data):
        name = data.get('name', '')
        jsonstore_data = data.get('data', {})
        is_public = data.get('is_public', False)

        user = self.context['request'].user
        obj = self.instance

        # public jsonstore name cannot be blank
        if is_public and not name:
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK)

        # jsonstore name not allowed
        if name and name in c.FORBIDDEN_JSONSTORE_NAMES:
            raise serializers.ValidationError(
                f"The name '{name}' cannot be used as a jsonstore name.")

        # user has too many jsonstores
        max_jsonstore_count = user.profile.get_max_jsonstore_count()
        if user.jsonstore_set.count() >= max_jsonstore_count:
            raise serializers.ValidationError(
                f"You have reached the maximum of {max_jsonstore_count} "
                "JSON stores. You cannot create any more JSON stores.")

        # duplicate jsonstore name
        jsonstores_with_same_name = \
            JsonStore.objects.filter(name=slugify(name))
        if is_public:
            different_user_public_jsonstores_with_same_name = \
                jsonstores_with_same_name.exclude(user=user)\
                    .filter(is_public=True)
            if different_user_public_jsonstores_with_same_name.exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE)
        if obj:
            same_user_jsonstores_with_same_name = \
                jsonstores_with_same_name.filter(user=user).exclude(pk=obj.pk)
            if name and same_user_jsonstores_with_same_name.exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE)
        else:
            if name and jsonstores_with_same_name.filter(user=user).exists():
                raise serializers.ValidationError(
                    c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE)

        # jsonstore size is too large
        jsonstore_data_size = h.get_obj_size(jsonstore_data)
        if jsonstore_data_size > user.profile.get_max_jsonstore_data_size():
            raise serializers.ValidationError(
                c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size))

        # jsonstore size will exceed user's total storage allowance
        if jsonstore_data_size + user.profile.get_all_jsonstores_data_size() >\
                user.profile.get_max_all_jsonstores_data_size():
            raise serializers.ValidationError(
                c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
                    user, jsonstore_data_size))

        return data

    def create(self, validated_data):
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
