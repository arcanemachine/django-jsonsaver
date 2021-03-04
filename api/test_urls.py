from django.urls import reverse, resolve
from django.test import SimpleTestCase


class ApiRootUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('api:api_root'), '/api/v1/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/api/v1/').view_name, 'api:api_root')


class JsonStoreViewSetUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('api:jsonstore-list'), '/api/v1/jsonstore/')
        self.assertEqual(
            reverse('api:jsonstore-detail',
                    kwargs={'pk': 1}),
            '/api/v1/jsonstore/1/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/api/v1/jsonstore/').view_name, 'api:jsonstore-list')
        self.assertEqual(
            resolve('/api/v1/jsonstore/1/').view_name, 'api:jsonstore-detail')


class JsonStoreNameDetailUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('api:jsonstore_detail_name',
                    kwargs={'jsonstore_name': 'test_jsonstore'}),
            '/api/v1/jsonstore/name/test_jsonstore/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/api/v1/jsonstore/name/test_jsonstore/').view_name,
            'api:jsonstore_detail_name')


class JsonStorePublicDetailUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('api:jsonstore_detail_public',
                    kwargs={'jsonstore_name': 'test_jsonstore'}),
            '/api/v1/jsonstore/public/test_jsonstore/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/api/v1/jsonstore/public/test_jsonstore/').view_name,
            'api:jsonstore_detail_public')
