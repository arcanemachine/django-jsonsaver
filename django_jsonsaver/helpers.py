import gc
import sys

from django.urls import reverse
from django.core.mail import send_mail
from math import ceil as math_ceil

from . import server_config


# utils
def get_next_url(request, url):
    """If request has a 'next' key, return it. Otherwise, return url."""
    if request.GET.get('next', None):
        return request.GET['next']
    return url


def get_obj_size(obj):  # https://stackoverflow.com/a/53705610/
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0
    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))
        new_refr = {o_id: o for o_id, o in all_refr
                    if o_id not in marked
                    and not isinstance(o, type)}
        obj_q = new_refr.values()
        marked.update(new_refr.keys())
    return sz


def kb_to_bytes(kb):
    """Converts bytes to kilobytes. Rounds up to the nearest integer."""
    if not isinstance(kb, (int, float)):
        raise TypeError("kb must be a numeric value")
    return math_ceil(kb * 1024)


def bytes_to_kb(bt):
    """Converts kilobytes to bytes. Rounds up to the nearest integer."""
    if not isinstance(bt, (int, float)):
        raise TypeError("bt must be a numeric value")
    return math_ceil(bt / 1024)


# email
def send_test_email(recipient):
    subject = "Test Message"
    body = "Test message sent successfully!"
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [recipient]
    return send_mail(subject, body, sender, recipient)


def send_contact_us_email(name, from_email, message):
    subject = f"{server_config.PROJECT_NAME} Contact Form: Submitted by {name}"
    body = f"Name: {name}\nEmail: {from_email}\n\nMessage: {message}"
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [server_config.CONTACT_FORM_EMAIL_RECIPIENT]
    return send_mail(subject, body, sender, recipient)


def send_welcome_email(recipient, activation_code):
    subject = f"{server_config.PROJECT_NAME}: Activate your account"
    body = "Welcome to jsonSaver!\n\n" +\
        "Please visit the following link to activate your account:\n\n" +\
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_activate', kwargs={
                'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [recipient]
    return send_mail(subject, body, sender, recipient)


def send_email_update_email(recipient, activation_code):
    subject = f"{server_config.PROJECT_NAME}: Confirm your new email address"
    body = "Please visit the following link to confirm your " +\
        "new email address:\n\n" + server_config.BACKEND_SERVER_URL + \
        reverse('users:user_update_email_confirm',
                kwargs={'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [recipient]
    return send_mail(subject, body, sender, recipient)


def send_user_username_recover_email(email, username):
    subject = f"{server_config.PROJECT_NAME}: Forgot your username?"
    body = f"Your username is '{username}'.\n\n" +\
        "You may login to your account here: " +\
        server_config.BACKEND_SERVER_URL + reverse('users:login')
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]
    return send_mail(subject, body, sender, recipient)
