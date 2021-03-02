# constants
JSONSTORE_LIST_PAGINATE_BY = 25
FORBIDDEN_JSONSTORE_NAMES = ['find']
JSONSTORE_NAME_MAX_LENGTH = 128


# testing
TEST_USER_USERNAME = 'test_user'
TEST_USER_FIRST_NAME = 'Test'
TEST_USER_LAST_NAME = 'User'
TEST_USER_EMAIL = 'test_user@email.com'
TEST_USER_PASSWORD = 'my_password321'
TEST_JSONSTORE_NAME = 'test_jsonstore'
TEST_JSONSTORE_DATA = {'message': 'Test jsonstore data'}


# strings

DJANGO_JSONSAVER_CONTACT_US_FORM_SUCCESS_MESSAGE =\
    "Your message has been received. Thank you for your feedback."

STORES_JSONSTORE_LOOKUP_FORM_LABEL = "Find your JSON store by name"
STORES_JSONSTORE_LOOKUP_PUBLIC_FORM_LABEL = "Find a public JSON store by name"
STORES_JSONSTORE_LOOKUP_FORM_HELP_TEXT =\
    "Your query will be converted to a URL-friendly format. "\
    "e.g. 'My Public STORE!' &rarr; 'my-public-store'"

FORM_ERROR_JSONSTORE_NAME_DUPLICATE =\
    "You cannot have multiple JSON stores with the same name."
FORM_ERROR_JSONSTORE_PUBLIC_NAME_BLANK =\
    "Publicly-accessible JSON stores must be given a name."
FORM_ERROR_JSONSTORE_PUBLIC_NAME_DUPLICATE =\
    "This publicly-accessible JSON store name is already in use."

FORM_FIELD_CAPTCHA_HELP_TEXT = "Please confirm that you are a human "\
    "by entering the letters seen in the picture."

MODEL_JSONSTORE_NAME_HELP_TEXT =\
    "Name will be lowercased and hyphenated for use in URLs."
MODEL_JSONSTORE_IS_PUBLIC_HELP_TEXT =\
    "Allow this JSON store to be publicly accessible by name."


def FORM_ERROR_JSONSTORE_DATA_SIZE_OVER_MAX(user, store_data_size):
    max_jsonstore_data_size_in_kb =\
        user.profile.get_max_jsonstore_data_size_in_kb()
    rounded_jsonstore_data_size = round(store_data_size / 1024, 2)
    return f"The maximum data size per store for your account is "\
        f"{max_jsonstore_data_size_in_kb} KB. The disk size of your entered data "\
        f"data is {rounded_jsonstore_data_size} KB."


def FORM_ERROR_ALL_JSONSTORES_DATA_SIZE_OVER_MAX(user, jsonstore_data_size):
    max_all_jsonstores_data_size_in_kb =\
        user.profile.get_max_all_jsonstores_data_size_in_kb()
    rounded_jsonstore_data_size = round(jsonstore_data_size / 1024, 2)
    jsonstore_data_size_excess =\
        round(abs(rounded_jsonstore_data_size -
              max_all_jsonstores_data_size_in_kb), 2)
    return f"The maximum storage capacity for all your JSON stores is "\
        f"{max_all_jsonstores_data_size_in_kb} KB. The disk size of your "\
        f"entered data is {rounded_jsonstore_data_size} KB which is "\
        f"{jsonstore_data_size_excess} KB too large."
