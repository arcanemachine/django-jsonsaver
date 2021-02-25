from django.urls import reverse
from django.core.mail import send_mail

from . import server_config


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
