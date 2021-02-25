# constants
JSONSTORE_DATA_MAX_SIZE = 1024 * 100
JSONSTORE_PAGINATE_BY = 25

# strings
FORBIDDEN_STORE_NAMES = ['find']

FORM_ERROR_STORE_DATA_OVER_MAX_SIZE = \
    f"Maximum store data size is {int(JSONSTORE_DATA_MAX_SIZE / 1024)} KB."
FORM_ERROR_STORE_NAME_DUPLICATE = \
    "You cannot have multiple stores with the same name."
FORM_ERROR_STORE_PUBLIC_NAME_BLANK = \
    "Publicly-accessible stores must be given a name."
FORM_ERROR_STORE_PUBLIC_NAME_DUPLICATE = \
    "This publicly-accessible store name is already in use."

FORM_FIELD_CAPTCHA_HELP_TEXT = "Please confirm that you are a human "\
    "by entering the letters seen in the picture."

