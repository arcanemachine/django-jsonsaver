from celery.decorators import task
from celery.utils.log import get_task_logger
from django_jsonsaver.helpers import send_welcome_email

logger = get_task_logger(__name__)


@task(name="send_welcome_email_task")
def send_welcome_email_task(email, username, activation_code):
    logger.info(f'Sent welcome email to {email}')
    return send_welcome_email(email, username, activation_code)
