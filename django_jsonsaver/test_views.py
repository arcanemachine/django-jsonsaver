from django.core import mail
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from html import unescape

from . import views

class ProjectRootViewTest(SimpleTestCase):
    def setUp(self):
        self.current_test_url = reverse('project_root')
        self.response = self.client.get(self.current_test_url)
        self.view = self.response.context['view']

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(
            self.view.__class__.__name__, 'ProjectRootTemplateView')

    def test_parent_class_name(self):
        self.assertEqual(
            self.view.__class__.__bases__[-1].__name__, 'TemplateView')

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'project_root.html')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)


class ContactUsFormViewTest(TestCase):
    def setUp(self):
        self.current_test_url = reverse('contact_us')
        self.response = self.client.get(self.current_test_url)
        self.view = self.response.context['view']

    # view attributes
    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'contact_us.html')

    def test_form_class_name(self):
        self.assertEqual(self.view.form_class.__name__, 'ContactUsForm')

    def test_form_success_message(self):
        self.assertEqual(
            self.view.success_message,
            "Your message has been received. Thank you for your feedback.")

    # form_valid()
    def test_form_valid(self):
        # covered by test_contact_form_submitted
        pass

    # get_success_url()
    def test_method_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)

    # functional tests
    def test_valid_contact_form_submitted(self):
        valid_contact_form_data = {
            'first_name': 'Test User',
            'email': 'test_user@email.com',
            'message': 'Test Message',
            'captcha_0': 'test',
            'captcha_1': 'PASSED'}
        self.response = self.client.post(
            self.current_test_url, valid_contact_form_data)

        # contact_us email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("jsonSaver Contact Form", mail.outbox[0].subject)

        # user is redirected to project_root
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/')

        # page contains success_message
        self.response = self.client.get(self.response.url)
        self.html = unescape(self.response.content.decode('utf-8'))
        self.assertIn(self.view.success_message, self.html)

    def test_invalid_contact_form_submitted_honeypot_field_filled(self):
        invalid_contact_form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test_user@email.com',
            'message': 'Test Message',
            'captcha_0': 'test',
            'captcha_1': 'PASSED'}
        self.response = self.client.post(
            self.current_test_url, invalid_contact_form_data)

        # no email sent
        self.assertEqual(len(mail.outbox), 0)

        # user is redirected to project_root
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/')

        # page contains success_message
        self.response = self.client.get(self.response.url)
        self.html = unescape(self.response.content.decode('utf-8'))
        self.assertIn(self.view.success_message, self.html)


class TermsOfUseTemplateViewTest(SimpleTestCase):
    def setUp(self):
        self.current_test_url = reverse('terms_of_use')
        self.response = self.client.get(self.current_test_url)

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'terms_of_use.html')


class PrivacyPolicyTemplateViewTest(SimpleTestCase):
    def setUp(self):
        self.current_test_url = reverse('privacy_policy')
        self.response = self.client.get(self.current_test_url)

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'privacy_policy.html')
