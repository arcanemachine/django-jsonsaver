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

        # public store name cannot be blank
        if is_public and not name:
            raise serializers.ValidationError(
                c.FORM_ERROR_STORE_PUBLIC_NAME_BLANK)

        # store name not allowed
        if name and name in c.FORBIDDEN_STORE_NAMES:
            raise serializers.ValidationError(
                f"The name '{name}' cannot be used as a store name.")

        # user has too many stores
        max_store_count = user.profile.get_max_store_count()
        if user.jsonstore_set.count() >= max_store_count:
            raise serializers.ValidationError(
                f"You have reached the maximum of {max_store_count} "
                "JSON stores. You cannot create any more stores.")

        # duplicate store name
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

        # store size is too large
        store_data_size = helpers.get_obj_size(store_data)
        if store_data_size > user.profile.get_max_store_data_size():
            raise serializers.ValidationError(
                c.FORM_ERROR_STORE_DATA_SIZE_OVER_MAX(user, store_data_size))

        # store size will exceed user's total storage allowance
        if store_data_size + user.profile.get_all_stores_data_size() > \
                user.profile.get_max_all_stores_data_size():
            raise serializers.ValidationError(
                c.FORM_ERROR_ALL_STORES_DATA_SIZE_OVER_MAX(
                    user, store_data_size))

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
