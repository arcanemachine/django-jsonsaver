# constants
JSONSTORE_LIST_PAGINATE_BY = 25
FORBIDDEN_STORE_NAMES = ['find']
JSONSTORE_NAME_MAX_LENGTH = 128


# testing
TEST_USER_USERNAME = 'test_user'
TEST_USER_FIRST_NAME = 'Test'
TEST_USER_LAST_NAME = 'User'
TEST_USER_EMAIL = 'test_user@email.com'
TEST_USER_PASSWORD = 'my_password321'
TEST_JSONSTORE_NAME = 'test_jsonstore'
TEST_JSONSTORE_DATA = {'message': 'test-message'}


# strings

DJANGO_JSONSAVER_CONTACT_US_FORM_SUCCESS_MESSAGE =\
    "Your message has been received. Thank you for your feedback."

STORES_JSONSTORE_LOOKUP_FORM_LABEL = "Find your JSON store by name"
STORES_JSONSTORE_LOOKUP_PUBLIC_FORM_LABEL = "Find a public JSON store by name"
STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT =\
    "Your query will be converted to a URL-friendly format. "\
    "e.g. 'My Public STORE!' &rarr; 'my-public-store'"

FORM_ERROR_STORE_NAME_DUPLICATE =\
    "You cannot have multiple stores with the same name."
FORM_ERROR_STORE_PUBLIC_NAME_BLANK =\
    "Publicly-accessible stores must be given a name."
FORM_ERROR_STORE_PUBLIC_NAME_DUPLICATE =\
    "This publicly-accessible store name is already in use."

FORM_FIELD_CAPTCHA_HELP_TEXT = "Please confirm that you are a human "\
    "by entering the letters seen in the picture."

MODEL_JSONSTORE_NAME_HELP_TEXT =\
    "Name will be lowercased and hyphenated for use in URLs."
MODEL_JSONSTORE_IS_PUBLIC_HELP_TEXT =\
    "Allow this store to be publicly accessible by name."


def FORM_ERROR_STORE_DATA_SIZE_OVER_MAX(user, store_data_size):
    max_store_data_size_in_kb =\
        user.profile.get_max_store_data_size_in_kb()
    rounded_store_data_size = round(store_data_size / 1024, 2)
    return f"The maximum data size per store for your account is "\
        f"{max_store_data_size_in_kb} KB. The disk size of your entered data "\
        f"is {rounded_store_data_size} KB. Please consider upgrading "\
        "your account if you need to use larger stores."


def FORM_ERROR_ALL_STORES_DATA_SIZE_OVER_MAX(user, store_data_size):
    max_all_stores_data_size_in_kb =\
        user.profile.get_max_all_stores_data_size_in_kb()
    rounded_store_data_size = round(store_data_size / 1024, 2)
    store_data_size_excess =\
        round(abs(rounded_store_data_size - max_all_stores_data_size_in_kb), 2)
    return f"The maximum storage capacity for all your JSON stores is "\
        f"{max_all_stores_data_size_in_kb} KB. The disk size of your "\
        f"entered data is {rounded_store_data_size} KB which is "\
        f"{store_data_size_excess} KB too large."
