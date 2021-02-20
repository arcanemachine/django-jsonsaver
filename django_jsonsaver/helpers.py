from django.urls import reverse
from django.core.mail import send_mail

from . import server_config


def send_welcome_email(user):
    subject = "jsonSaver: Activate your account"
    message = "Welcome to jsonSaver!\n\n" \
        "Please visit the following link to activate your account:\n\n" + \
        server_config.SERVER_LOCATION + reverse('users:user_confirm', kwargs={
            'confirmation_code': user.profile.confirmation_code})
    sender = server_config.SERVER_EMAIL
    recipient = [user.email]

    send_mail(subject, message, sender, recipient)
