from django_jsonsaver import constants as c


# JSONSTORE #

# public jsonstore name cannot be blank
def jsonstore_public_name_cannot_be_blank(name, is_public):
    if is_public and not name:
        return True


# forbidden jsonstore name not allowed
def jsonstore_forbidden_name_not_allowed(name):
    if name in c.JSONSTORE_FORBIDDEN_NAMES:
        return True


# user has too many jsonstores
def jsonstore_user_jsonstore_count_over_max(user, user_max_jsonstore_count):
    if user.jsonstore_set.count() >= user_max_jsonstore_count:
        return True


# jsonstore_name_duplicate_same_user_create
def jsonstore_name_duplicate_same_user_create(
        name, user, obj, stores_with_same_name):
    if not obj:
        if name and stores_with_same_name.filter(user=user).exists():
            return True


# jsonstore_name_duplicate_same_user_update
def jsonstore_name_duplicate_same_user_update(
        name, user, obj, stores_with_same_name):
    if obj:
        same_user_jsonstores_with_same_name = \
            stores_with_same_name.filter(user=user).exclude(pk=obj.pk)
        if name and same_user_jsonstores_with_same_name.exists():
            return True


# jsonstore_public_name_duplicate
def jsonstore_public_name_duplicate(
        name, is_public, user, stores_with_same_name):
    if is_public:
        other_user_public_jsonstores_with_same_name = \
            stores_with_same_name.exclude(user=user).filter(is_public=True)
        if other_user_public_jsonstores_with_same_name.exists():
            return True


# jsonstore data size over max
def jsonstore_data_size_over_max(jsonstore_data, user, jsonstore_data_size):
    if jsonstore_data_size >= user.profile.get_max_jsonstore_data_size():
        return True


# jsonstore size will exceed user's total storage allowance
def jsonstore_all_jsonstores_data_size_over_max(user, jsonstore_data_size):
    if jsonstore_data_size + \
            user.profile.get_all_jsonstores_data_size_in_kb() >=\
            user.profile.get_max_jsonstore_all_jsonstores_data_size_in_kb():
        return True
