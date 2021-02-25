import gc
import sys

from django.urls import reverse
from django.core.mail import send_mail

from . import server_config


# https://stackoverflow.com/a/53705610/
def get_obj_size(obj):
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


def send_welcome_email(email, username, activation_code):
    subject = "jsonSaver: Activate your account"
    message = "Welcome to jsonSaver!\n\n" +\
        "Please visit the following link to activate your account:\n\n" +\
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_activate', kwargs={
                'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]
    return send_mail(subject, message, sender, recipient)


def send_email_update_email(email, username, activation_code):
    subject = "jsonSaver: Confirm your new email address"
    message = "Please visit the following link to confirm your " +\
        "new email address:\n\n" +\
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_update_email_confirm', kwargs={
                'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]
    return send_mail(subject, message, sender, recipient)


def send_user_username_recover_email(email, username):
    subject = "jsonSaver: Your forgotten username"
    message = f"Your username is '{username}'.\n\n" +\
        "You may login to your account here: " +\
        server_config.BACKEND_SERVER_URL + reverse('users:login')
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]
    return send_mail(subject, message, sender, recipient)
