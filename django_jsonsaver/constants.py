from .server_config import MAX_STORE_SIZE_IN_KB

# constants
JSONSTORE_COUNT_MAX_FREE = 1
JSONSTORE_DATA_SIZE_MAX = 1024 * MAX_STORE_SIZE_IN_KB
JSONSTORE_PAGINATE_BY = 25

# strings
FORBIDDEN_STORE_NAMES = ['find']

FORM_ERROR_STORE_DATA_SIZE_OVER_MAX = \
    f"Maximum store data size is {int(JSONSTORE_DATA_SIZE_MAX / 1024)} KB."
FORM_ERROR_STORE_NAME_DUPLICATE = \
    "You cannot have multiple stores with the same name."
FORM_ERROR_STORE_PUBLIC_NAME_BLANK = \
    "Publicly-accessible stores must be given a name."
FORM_ERROR_STORE_PUBLIC_NAME_DUPLICATE = \
    "This publicly-accessible store name is already in use."

FORM_FIELD_CAPTCHA_HELP_TEXT = "Please confirm that you are a human "\
    "by entering the letters seen in the picture."

