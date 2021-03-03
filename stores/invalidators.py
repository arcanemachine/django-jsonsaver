from django_jsonsaver import constants as c


# public store name cannot be blank
def public_jsonstore_name_cannot_be_blank(name, is_public):
    if is_public and not name:
        return True


# forbidden jsonstore name not allowed
def forbidden_jsonstore_name_not_allowed(name):
    if name and name in c.FORBIDDEN_JSONSTORE_NAMES:
        return True


# user has too many stores
def user_has_too_many_stores(user, user_max_jsonstore_count):
    if user.jsonstore_set.count() >= user_max_jsonstore_count:
        return True


# store_name_duplicate_same_user_create
def jsonstore_name_duplicate_same_user_create(
        name, user, obj, stores_with_same_name):
    if not obj:
        if name and stores_with_same_name.filter(user=user).exists():
            return True


# store_name_duplicate_same_user_update
def jsonstore_name_duplicate_same_user_update(
        name, user, obj, stores_with_same_name):
    if obj:
        same_user_jsonstores_with_same_name = \
            stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
        if name and same_user_jsonstores_with_same_name.exists():
            return True


# public_jsonstore_name_duplicate
def jsonstore_public_name_duplicate_other_user(
        name, is_public, user, stores_with_same_name):
    if is_public:
        other_user_public_jsonstores_with_same_name = \
            stores_with_same_name.exclude(user=user).filter(is_public=True)
        if other_user_public_jsonstores_with_same_name.exists():
            return True


# jsonstore data size over max
def jsonstore_data_size_over_max(jsonstore_data, user, jsonstore_data_size):
    if jsonstore_data_size > user.profile.get_max_jsonstore_data_size():
        return True


# jsonstore size will exceed user's total storage allowance
def all_jsonstores_data_size_over_max(user, jsonstore_data_size):
    if jsonstore_data_size + user.profile.get_all_jsonstores_data_size() >\
            user.profile.get_max_all_jsonstores_data_size():
        return True
