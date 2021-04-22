from os.path import join as os_path_join
from pathlib import Path

from .helpers import kb_to_bytes

PROJECT_NAME = 'jsonSaver'

BACKEND_SERVER_TYPE = 'dev'
SERVER_EMAIL = 'no-reply@your-domain.com'
CONTACT_FORM_EMAIL_RECIPIENT = 'your-email@your-domain.com'

BACKEND_SERVER_PROTOCOL = 'http://'
BACKEND_SERVER_IP = '192.168.1.120'
BACKEND_SERVER_PORT = '8000'
BACKEND_SERVER_URL = f'{BACKEND_SERVER_PROTOCOL}{BACKEND_SERVER_IP}' + \
    f'{":" + BACKEND_SERVER_PORT if BACKEND_SERVER_PORT else ""}'

BASE_DIR = str(Path(__file__).resolve().parent.parent)
DEBUG = True
TIME_ZONE = 'UTC'

TEMPLATE_DIRS = os_path_join(BASE_DIR, 'templates')

# celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_TIMEZONE = 'UTC'

# corsheaders
CORS_ALLOW_ALL_ORIGINS = True

# database - choose 'sqlite' or 'postgres'
USE_DATABASE = 'sqlite'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'

# rest_framework
BROWSABLE_API = True if DEBUG else False

# static
STATICFILES_DIRS = [os_path_join(BASE_DIR, 'static')]
STATIC_ROOT = None

# user limits
MAX_JSONSTORE_COUNT_USER_FREE = 50
MAX_JSONSTORE_DATA_SIZE_USER_FREE = kb_to_bytes(1024)
MAX_JSONSTORE_ALL_JSONSTORES_DATA_SIZE_USER_FREE = kb_to_bytes(1024)

THROTTLE_RATE_ANON = '100/day'
THROTTLE_RATE_USER = '1000/day'
