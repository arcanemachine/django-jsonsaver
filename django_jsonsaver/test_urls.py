from django.urls import reverse, resolve
from django.test import SimpleTestCase


class ProjectRootTemplateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('project_root'), '/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/').view_name, 'project_root')


class ContactUsFormViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('contact_us'), '/contact-us/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/contact-us/').view_name, 'contact_us')


class FaqTemplateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('faq'), '/faq/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/faq/').view_name, 'faq')


class PrivacyPolicyTemplateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('privacy_policy'), '/privacy-policy/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/privacy-policy/').view_name, 'privacy_policy')


class TermsOfUseTemplateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('terms_of_use'), '/terms-of-use/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/terms-of-use/').view_name, 'terms_of_use')
