from django.urls import reverse
from django.core.mail import send_mail

from . import server_config


def send_welcome_email(email, username, activation_code):
    subject = "jsonSaver: Activate your account"
    message = f"Welcome to jsonSaver! Your username is {username}.\n\n" +\
        "Please visit the following link to activate your account:\n\n" +\
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_activate', kwargs={
                'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]

    return send_mail(subject, message, sender, recipient)


def send_email_update_email(email, username, activation_code):
    subject = "jsonSaver: Confirm your email address"
    message = "Please visit the following link to confirm your email:\n\n" +\
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_update_email_confirm', kwargs={
                'activation_code': activation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]

    return send_mail(subject, message, sender, recipient)
