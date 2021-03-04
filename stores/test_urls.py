from django.urls import reverse, resolve
from django.test import SimpleTestCase


class JsonStoreListViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_list'), '/stores/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/').view_name, 'stores:jsonstore_list')


class JsonStoreCreateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_create'), '/stores/new/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/').view_name, 'stores:jsonstore_list')


class JsonStoreDetailViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_detail', kwargs={
            'jsonstore_pk': 1}), '/stores/1/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/1/').view_name, 'stores:jsonstore_detail')


class JsonStoreLookupViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('stores:jsonstore_lookup'), '/stores/name/find/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/name/find/').view_name, 'stores:jsonstore_lookup')


class JsonStoreNameDetailViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_detail_name', kwargs={
            'jsonstore_name': 'test_jsonstore'}),
            '/stores/name/test_jsonstore/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/name/test_jsonstore/').view_name,
            'stores:jsonstore_detail_name')


class JsonStorePublicLookupViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('stores:jsonstore_lookup_public'), '/stores/public/find/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/public/find/').view_name,
            'stores:jsonstore_lookup_public')


class JsonStorePublicDetailViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_detail_public', kwargs={
            'jsonstore_name': 'test_jsonstore'}),
            '/stores/public/test_jsonstore/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/public/test_jsonstore/').view_name,
            'stores:jsonstore_detail_public')


class JsonStoreUpdateUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_update', kwargs={
            'jsonstore_pk': 1}), '/stores/1/update/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/1/update/').view_name, 'stores:jsonstore_update')


class JsonStoreDeleteUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('stores:jsonstore_delete', kwargs={
            'jsonstore_pk': 1}), '/stores/1/delete/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/stores/1/delete/').view_name, 'stores:jsonstore_delete')
