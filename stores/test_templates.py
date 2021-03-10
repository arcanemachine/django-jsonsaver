from bs4 import BeautifulSoup as bs
from django.urls import reverse
from django.test import TestCase

from django_jsonsaver import constants as c, factories as f


class JsonStoreCreateTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('stores:jsonstore_create')

    def setUp(self):
        self.assertTrue(self.client.login(username=self.test_user.username,
                                          password=c.TEST_USER_PASSWORD))

    def test_show_alert_for_user_with_max_store_count(self):
        while self.test_user.jsonstore_set.count() < \
                self.test_user.profile.get_max_jsonstore_count():
            f.JsonStoreFactory(user=self.test_user)
        response = self.client.get(self.test_url)
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNotNone(soup.find(id='alert-user-max-store-count'))

    def test_do_not_show_alert_if_user_not_has_max_store_count(self):
        response = self.client.get(self.test_url)
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNone(soup.find(id='alert-user-max-store-count'))


class JsonStoreListTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_url = reverse('stores:jsonstore_list')

    def setUp(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username, password=c.TEST_USER_PASSWORD))

    def test_small_item_count_is_not_paginated(self):
        response = self.client.get(self.test_url)
        self.assertFalse(response.context['is_paginated'])
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNone(soup.find(id='page-link-first'))
        self.assertIsNone(soup.find(id='page-link-last'))

    def test_large_item_count_is_paginated(self):
        while self.test_user.jsonstore_set.count() < \
                (c.JSONSTORE_LIST_PAGINATE_BY + 1):
            f.JsonStoreFactory(user=self.test_user)
        response = self.client.get(self.test_url)
        self.assertTrue(response.context['is_paginated'])
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNotNone(soup.find(id='page-link-last'))


class JsonStoreDetailTemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.test_jsonstore = \
            f.JsonStoreFactory(user=cls.test_user, is_public=True)
        cls.test_url = reverse('stores:jsonstore_detail', kwargs={
            'jsonstore_pk': cls.test_jsonstore.pk})

    def test_public_jsonstore_shows_public_alert_to_store_owner(self):
        self.assertTrue(self.client.login(
            username=self.test_user.username,
            password=c.TEST_USER_PASSWORD))
        response = self.client.get(self.test_url)
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNone(soup.find('alert-info-jsonstore-is-public'))

    def test_public_jsonstore_shows_no_public_alert_to_non_store_owner(self):
        response = self.client.get(self.test_url)
        html = response.content.decode('utf-8')
        soup = bs(html, 'html5lib')
        self.assertIsNone(soup.find('alert-info-jsonstore-is-public'))
