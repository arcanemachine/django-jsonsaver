from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import JsonStore
from django_jsonsaver import constants as c, helpers as h


def validate(self):
    jsonstore_data = self.cleaned_data.get('data')
    name = self.cleaned_data.get('name')
    is_public = self.data.get('is_public')

    user = self.user
    obj = self.obj


def invalidate_public_jsonstore_name_cannot_be_blank(is_public, name):
    # public store name cannot be blank
    if is_public and not name:
        return True
#         self.add_error('name', ValidationError(
#             c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK,
#             code='public_jsonstore_name_cannot_be_blank'))


# forbidden jsonstore name not allowed
def invalidate_forbidden_jsonstore_name_not_allowed(name):
    if name and name in c.FORBIDDEN_JSONSTORE_NAMES:
        return True
#         self.add_error('name', ValidationError(
#             "The name '%(name)s' cannot be used as a store name.",
#             code='forbidden_jsonstore_name_not_allowed',
#             params={'name': name}))


# user has too many stores
def invalidate_user_has_too_many_stores(user):
    max_jsonstore_count = user.profile.get_max_jsonstore_count()
    if user.jsonstore_set.count() >= max_jsonstore_count:
        return True
#         self.add_error(None, ValidationError(
#             "You have reached the maximum of %(max_jsonstore_count)s "
#             "JSON stores. You cannot create any more stores.",
#             code='user_has_too_many_jsonstores',
#             params={'max_jsonstore_count': max_jsonstore_count}))


# store name duplicate
def invalidate_store_name_duplicate(
    stores_with_same_name = JsonStore.objects.filter(name=slugify(name))
    if is_public:
        other_user_public_jsonstores_with_same_name = \
            stores_with_same_name.exclude(user=user).filter(is_public=True)
        if other_user_public_jsonstores_with_same_name.exists():
            # store public name duplicate
#             self.add_error('name', ValidationError(
#                 c.FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE,
#                 code='jsonstore_public_name_duplicate_other_user'))
    if obj:
        same_user_jsonstores_with_same_name = \
            stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
        if name and same_user_jsonstores_with_same_name.exists():
            # store name duplicate
#             self.add_error('name', ValidationError(
#                 c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
#                 code='jsonstore_name_duplicate_same_user'))
    else:
        if name and stores_with_same_name.filter(user=user).exists():
            # store name duplicate
#             self.add_error('name', ValidationError(
#                 c.FORM_ERROR_JSONSTORE_NAME_DUPLICATE,
#                 code='jsonstore_name_duplicate_same_user'))

    # store data size over max
    jsonstore_data_size = h.get_obj_size(jsonstore_data)
    if jsonstore_data_size > user.profile.get_max_jsonstore_data_size():
#         self.add_error('data', ValidationError(
#             c.FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(
#                 user, jsonstore_data_size),
#             code='jsonstore_data_size_over_max'))

    # store size will exceed user's total storage allowance
    if jsonstore_data_size + user.profile.get_all_jsonstores_data_size() >\
            user.profile.get_max_all_jsonstores_data_size():
#         self.add_error('data', ValidationError(
#             c.FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(
#                 user, jsonstore_data_size),
#             code='all_jsonstores_data_size_over_max'))

    return self.cleaned_data


