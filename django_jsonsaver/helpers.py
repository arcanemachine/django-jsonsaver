from django.urls import reverse
from django.core.mail import send_mail

from . import server_config


def send_welcome_email(email, confirmation_code):
    subject = "jsonSaver: Activate your account"
    message = "Welcome to jsonSaver!\n\n" \
        "Please visit the following link to activate your account:\n\n" + \
        server_config.BACKEND_SERVER_URL + \
        reverse('users:user_confirm', kwargs={
                'confirmation_code': confirmation_code})
    sender = server_config.BACKEND_SERVER_EMAIL
    recipient = [email]

    return send_mail(subject, message, sender, recipient)
