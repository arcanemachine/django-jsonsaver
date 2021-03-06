# constants
JSONSTORE_LIST_PAGINATE_BY = 25
JSONSTORE_FORBIDDEN_NAMES = ['find']
JSONSTORE_NAME_MAX_LENGTH = 128


# testing
TEST_MESSAGE = 'Test Message'

TEST_JSONSTORE_NAME = 'test_jsonstore'
TEST_JSONSTORE_DATA = {'message': 'Test jsonstore data'}

TEST_USER_USERNAME = 'test_user'
TEST_USER_ADMIN_USERNAME = 'admin_user'
TEST_USER_FIRST_NAME = 'Test'
TEST_USER_LAST_NAME = 'User'
TEST_USER_FULL_NAME = f'{TEST_USER_FIRST_NAME} {TEST_USER_LAST_NAME}'
TEST_USER_EMAIL = 'test_user@email.com'
TEST_USER_PASSWORD = 'my_password321'

# STRINGS #

# project_folder
DJANGO_JSONSAVER_CONTACT_US_FORM_SUCCESS_MESSAGE = \
    "Your message has been received. Thank you for your feedback."

# captcha
FORM_FIELD_CAPTCHA_HELP_TEXT = "Please confirm that you are a human "\
    "by entering the letters seen in the picture."

# JsonStore
MODEL_JSONSTORE_NAME_HELP_TEXT = \
    "Name will be lowercased and hyphenated for use in URLs."
MODEL_JSONSTORE_IS_PUBLIC_HELP_TEXT = \
    "Allow this JSON store to be publicly accessible by name."

STORES_JSONSTORE_LOOKUP_FORM_LABEL = "Find your JSON store by name"
STORES_JSONSTORE_PUBLIC_LOOKUP_FORM_LABEL = "Find a public JSON store by name"
STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT = \
    "Your query will be converted to a URL-friendly format. "\
    "e.g. 'My Public STORE!' &rarr; 'my-public-store'"
JSONSTORE_CREATE_SUCCESS_MESSAGE = "Store created successfully"
JSONSTORE_UPDATE_SUCCESS_MESSAGE = "Store updated successfully"
JSONSTORE_DELETE_SUCCESS_MESSAGE = "Store deleted successfully"

# User
USER_FORM_EMAIL_ERROR_DUPLICATE = \
    "This email address is registered to another account."
USER_FORM_EMAIL_ERROR_SAME_EMAIL = \
    "This email address is already registered to your account."
USER_VIEW_REGISTER_SUCCESS_MESSAGE = \
    "Success! Please check your email inbox for your confirmation message."
USER_VIEW_ACTIVATION_EMAIL_RESEND_ACCOUNT_ALREADY_ACTIVE = \
    "This account has already been activated."
USER_VIEW_ACTIVATION_EMAIL_RESEND_SUCCESS_MESSAGE = \
    "If the email address you entered matches an account that has not yet "\
    "been activated, then we have resent an activation email to that address."
USER_VIEW_USER_ACTIVATE_ACCOUNT_ALREADY_ACTIVE = \
    "Your account has already been activated."
USER_VIEW_USER_ACTIVATE_SUCCESS_MESSAGE = \
    "Account confirmed! You may now login."
USER_VIEW_LOGIN_SUCCESS_MESSAGE = "You are now logged in."
USER_VIEW_LOGIN_ACTIVATE_ACCOUNT_REMINDER = \
    "Your account has not been activated. "\
    "Please check your email inbox for your activation email."
USER_VIEW_DETAIL_PUBLIC_SAME_USER_IS_PRIVATE = \
    "Your account's visibility is set to private."

# Profile
PROFILE_MODEL_IS_PUBLIC_VERBOSE_NAME = "Make this profile publicly accessible"
PROFILE_MODEL_IS_PUBLIC_HELP_TEXT = \
    "If this setting is active, users can look up this profile " \
    "via your username and view all your public JSON stores."


FORM_ERROR_JSONSTORE_NAME_DUPLICATE = \
    "You cannot have multiple JSON stores with the same name."
FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK = \
    "Publicly-accessible JSON stores must be given a name."
FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE = \
    "This publicly-accessible JSON store name is already in use."


def FORM_ERROR_JSONSTORE_FORBIDDEN_NAME_NOT_ALLOWED(name):
    return f"The name '{name}' cannot be used as a jsonstore name."


def FORM_ERROR_JSONSTORE_USER_JSONSTORE_COUNT_OVER_MAX(
        user, user_max_jsonstore_count):
    return f"You have reached the maximum of {user_max_jsonstore_count} JSON "\
        "stores. You cannot create any more JSON stores."


def FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(user, store_data_size):
    max_jsonstore_data_size_in_kb = \
        user.profile.get_max_jsonstore_data_size_in_kb()
    rounded_jsonstore_data_size = round(store_data_size / 1024, 2)
    return f"The maximum data size per store for your account is "\
        f"{max_jsonstore_data_size_in_kb} KB. The disk size of your entered "\
        f"data is {rounded_jsonstore_data_size} KB."


def FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(user, jsonstore_data_size):
    max_jsonstore_all_jsonstores_data_size_in_kb = \
        user.profile.get_max_jsonstore_all_jsonstores_data_size_in_kb()
    rounded_jsonstore_data_size = round(jsonstore_data_size / 1024, 2)
    jsonstore_data_size_excess = \
        round(abs(jsonstore_data_size -
              max_jsonstore_all_jsonstores_data_size_in_kb), 2)
    return f"The maximum storage capacity for all your JSON stores is "\
        f"{max_jsonstore_all_jsonstores_data_size_in_kb} KB. The disk size "\
        f"of your entered data is {rounded_jsonstore_data_size} KB, which is "\
        f"{jsonstore_data_size_excess} KB too large."
