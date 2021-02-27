from celery.decorators import task
from celery.utils.log import get_task_logger

from django_jsonsaver import helpers as h

logger = get_task_logger(__name__)


@task(name="send_test_email_task")
def send_test_email_task(email):
    logger.info(f'Sent test email to {email}')
    return h.send_test_email(email)


@task(name="send_contact_us_email_task")
def send_contact_us_email_task(name, email, message):
    logger.info(f'Sent contact_us email from {name}')
    return h.send_contact_us_email(name, email, message)


@task(name="send_welcome_email_task")
def send_welcome_email_task(email, activation_code):
    logger.info(f'Sent welcome email to {email}')
    return h.send_welcome_email(email, activation_code)


@task(name="send_email_update_email_task")
def send_email_update_email_task(email, activation_code):
    logger.info(f'Sent email_update email to {email}')
    return h.send_email_update_email(email, activation_code)


@task(name="send_user_username_recover_email_task")
def send_user_username_recover_email_task(email, username):
    logger.info(f'Sent user_username_recover email to {email}')
    return h.send_user_username_recover_email(email, username)
