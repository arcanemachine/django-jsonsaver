from bs4 import BeautifulSoup as bs
from django.test import SimpleTestCase
from django.urls import reverse


class CookieNoticeTest(SimpleTestCase):
    """These tests use project_root.html as a proxy for base.html"""
    def test_template_contains_cookie_notice(self):
        response = self.client.get(reverse('project_root'))
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNotNone(soup.find(id='cookie-notice'))
