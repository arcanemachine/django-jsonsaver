from django.core import mail
from django.test import TestCase
from django.urls import reverse
from html import unescape

from . import constants as c, factories as f


class ProjectRootViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.current_test_url = reverse('project_root')
        self.response = self.client.get(self.current_test_url)
        self.view_instance = self.response.context['view']

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'project_root.html')

    def test_get_method_authenticated_user(self):
        self.client.login(
            username=c.TEST_USER_USERNAME, password=c.TEST_USER_PASSWORD)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'project_root.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__name__,
            'ProjectRootTemplateView')

    def test_parent_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[-1].__name__,
            'TemplateView')

    def test_template_name(self):
        self.assertEqual(self.view_instance.template_name, 'project_root.html')


class ContactUsFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.current_test_url = reverse('contact_us')
        self.response = self.client.get(self.current_test_url)
        self.view_instance = self.response.context['view']

    # view attributes
    def test_template_name(self):
        self.assertEqual(self.view_instance.template_name, 'contact_us.html')

    def test_parent_class_mixins(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[0].__name__,
            'SuccessMessageMixin')

    def test_parent_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[-1].__name__,
            'FormView')

    def test_form_class_name(self):
        self.assertEqual(
            self.view_instance.form_class.__name__, 'ContactUsForm')

    def test_form_success_message(self):
        self.assertEqual(
            self.view_instance.success_message,
            c.DJANGO_JSONSAVER_CONTACT_US_FORM_SUCCESS_MESSAGE)

    # form_valid()
    def test_form_valid(self):
        # covered by test_contact_form_submitted
        pass

    # get_success_url()
    def test_method_get_success_url(self):
        self.assertEqual(self.view_instance.get_success_url(), '/')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)

    def test_get_method_authenticated_user(self):
        self.client.login(
            username=c.TEST_USER_USERNAME, password=c.TEST_USER_PASSWORD)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)

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
        self.assertIn(self.view_instance.success_message, self.html)

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
        self.assertIn(self.view_instance.success_message, self.html)


class FaqTemplateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.current_test_url = reverse('faq')
        self.response = self.client.get(self.current_test_url)
        self.view_instance = self.response.context['view']

    # view attributes
    def test_parent_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[-1].__name__,
            'TemplateView')

    def test_template_name(self):
        self.assertEqual(self.view_instance.template_name, 'faq.html')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)

    def test_get_method_authenticated_user(self):
        self.client.login(
            username=c.TEST_USER_USERNAME, password=c.TEST_USER_PASSWORD)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)


class TermsOfUseTemplateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.current_test_url = reverse('terms_of_use')
        self.response = self.client.get(self.current_test_url)
        self.view_instance = self.response.context['view']

    # view attributes
    def test_parent_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[-1].__name__,
            'TemplateView')

    def test_template_name(self):
        self.assertEqual(self.view_instance.template_name, 'terms_of_use.html')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)

    def test_get_method_authenticated_user(self):
        self.client.login(
            username=c.TEST_USER_USERNAME, password=c.TEST_USER_PASSWORD)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)


class PrivacyPolicyTemplateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()

    def setUp(self):
        self.current_test_url = reverse('privacy_policy')
        self.response = self.client.get(self.current_test_url)
        self.view_instance = self.response.context['view']

    # view attributes
    def test_parent_class_name(self):
        self.assertEqual(
            self.view_instance.__class__.__bases__[-1].__name__,
            'TemplateView')

    def test_template_name(self):
        self.assertEqual(
            self.view_instance.template_name, 'privacy_policy.html')

    # request.GET
    def test_get_method_unauthenticated_user(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)

    def test_get_method_authenticated_user(self):
        self.client.login(
            username=c.TEST_USER_USERNAME, password=c.TEST_USER_PASSWORD)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response, self.view_instance.template_name)
