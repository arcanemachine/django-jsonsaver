from django.core import mail
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from unittest.mock import Mock

from . import \
    constants as c, factories as f, helpers as h, server_config as sc


class GetNextUrlTest(SimpleTestCase):
    def test_request_get_next_with_next_key_returns_next_value(self):
        request = Mock()
        request.GET = {'next': 'ok'}
        self.assertEqual(h.get_next_url(request, None), 'ok')

    def test_request_get_next_with_no_next_key_returns_url(self):
        request = Mock()
        request.GET = {}
        self.assertEqual(h.get_next_url(request, 'ok'), 'ok')


class KbToBytesTest(SimpleTestCase):
    def test_non_numeric_value_raises_typeerror(self):
        with self.assertRaises(TypeError):
            h.kb_to_bytes(None)

    # integer input
    def test_1_returns_1024(self):
        self.assertEqual(h.kb_to_bytes(1), 1024)

    def test_2_returns_2048(self):
        self.assertEqual(h.kb_to_bytes(2), 2048)

    # float input
    def test_float_returns_expected_integer_value(self):
        self.assertEqual(h.kb_to_bytes(0.5), 512)


class BytesToKbTest(SimpleTestCase):
    def test_non_numeric_value_raises_typeerror(self):
        with self.assertRaises(TypeError):
            h.bytes_to_kb(None)

    # integer input
    def test_1024_returns_1(self):
        self.assertEqual(h.bytes_to_kb(1024), 1)

    def test_2048_returns_2(self):
        self.assertEqual(h.bytes_to_kb(2048), 2)

    # float input
    def test_float_returns_expected_integer_value(self):
        self.assertEqual(h.bytes_to_kb(0.5), 1)


class SendEmailFunctionsTest(TestCase):
    def test_send_test_email(self):
        recipient = 'test@email.com'

        h.send_test_email(recipient)
        self.assertEqual(len(mail.outbox), 1)

        test_email = mail.outbox[0]
        self.assertEqual(test_email.subject, "Test Message")
        self.assertEqual(test_email.body, "Test message sent successfully!")
        self.assertEqual(test_email.from_email, sc.BACKEND_SERVER_EMAIL)
        self.assertEqual(test_email.to, [recipient])

    def test_send_contact_us_email(self):
        name = c.TEST_USER_FULL_NAME
        from_email = c.TEST_USER_EMAIL
        message = c.TEST_MESSAGE

        h.send_contact_us_email(name, from_email, message)
        self.assertEqual(len(mail.outbox), 1)

        test_email = mail.outbox[0]
        self.assertEqual(
            test_email.subject,
            f"{sc.PROJECT_NAME} Contact Form: Submitted by {name}")
        self.assertEqual(
            test_email.body,
            f"Name: {name}\nEmail: {from_email}\n\nMessage: {message}")
        self.assertEqual(test_email.from_email, sc.BACKEND_SERVER_EMAIL)
        self.assertEqual(test_email.to, [sc.CONTACT_FORM_EMAIL_RECIPIENT])

    def test_send_welcome_email(self):
        recipient = c.TEST_USER_USERNAME
        activation_code = 'test'

        h.send_welcome_email(recipient, activation_code)
        self.assertEqual(len(mail.outbox), 1)

        test_email = mail.outbox[0]
        self.assertEqual(
            test_email.subject, f"{sc.PROJECT_NAME}: Activate your account")
        self.assertEqual(
            test_email.body,
            f"Welcome to {sc.PROJECT_NAME}!\n\n" +
            "Please visit the following link to activate your account:\n\n" +
            sc.BACKEND_SERVER_URL +
            reverse('users:user_activate',
                    kwargs={'activation_code': activation_code}))
        self.assertEqual(test_email.from_email, sc.BACKEND_SERVER_EMAIL)
        self.assertEqual(test_email.to, [recipient])

    def test_send_email_update_email(self):
        recipient = c.TEST_USER_USERNAME
        activation_code = 'test'

        h.send_email_update_email(recipient, activation_code)
        self.assertEqual(len(mail.outbox), 1)

        test_email = mail.outbox[0]
        self.assertEqual(
            test_email.subject,
            f"{sc.PROJECT_NAME}: Confirm your new email address")
        self.assertEqual(
            test_email.body,
            "Please visit the following link to confirm your "
            "new email address:\n\n" + sc.BACKEND_SERVER_URL +
            reverse('users:user_update_email_confirm',
                    kwargs={'activation_code': activation_code}))
        self.assertEqual(test_email.from_email, sc.BACKEND_SERVER_EMAIL)
        self.assertEqual(test_email.to, [recipient])

    def test_send_user_username_recover_email(self):
        test_user = f.UserFactory()

        recipient = test_user.email
        username = test_user.username

        h.send_user_username_recover_email(recipient, username)
        self.assertEqual(len(mail.outbox), 1)

        test_email = mail.outbox[0]
        self.assertEqual(
            test_email.subject, f"{sc.PROJECT_NAME}: Forgot your username?")
        self.assertEqual(
            test_email.body,
            f"Your username is '{username}'.\n\n" +
            "You may login to your account here: " +
            sc.BACKEND_SERVER_URL + reverse('users:login'))
        self.assertEqual(test_email.from_email, sc.BACKEND_SERVER_EMAIL)
        self.assertEqual(test_email.to, [recipient])
