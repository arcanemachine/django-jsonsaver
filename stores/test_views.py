from django.test import TestCase
from django.urls import reverse
from html import unescape

from django_jsonsaver import constants as c, factories as f
from . import views


class JsonStoreListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = f.UserFactory()
        cls.current_test_url = reverse('stores:jsonstore_list')
        cls.view = views.JsonStoreListView

    def setUp(self):
        self.client.login(username=self.test_user.username,
                          password=c.TEST_USER_PASSWORD)
        self.response = self.client.get(self.current_test_url)
        self.context = self.response.context
        self.html = unescape(self.response.content.decode('utf-8'))
        self.view_instance = self.response.context['view']

    # request.GET
    def test_request_get(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed('stores/jsonstore_list.html')

    # view attributes
    def test_view_class_name(self):
        self.assertEqual(self.view.__name__, 'JsonStoreListView')

    def test_view_mixins(self):
        self.assertEqual(self.view.__bases__[0].__name__, 'LoginRequiredMixin')

    def test_view_parent_class(self):
        self.assertEqual(self.view.__bases__[1].__name__, 'ListView')

    def test_view_model_name(self):
        self.assertEqual(self.view.model.__name__, 'JsonStore')

    def test_view_context_object_name(self):
        self.assertEqual(self.view.context_object_name, 'jsonstores')

    def test_view_paginate_by(self):
        self.assertEqual(self.view.paginate_by, c.JSONSTORE_LIST_PAGINATE_BY)

    # METHODS #

    # get_queryset()
    def test_method_get_queryset(self):
        for i in range(3):
            f.JsonStoreFactory(user=self.test_user)
        self.setUp()
        qs_repr = \
            repr(self.test_user.jsonstore_set.order_by('-updated_at'))
        self.assertEqual(repr(self.view_instance.get_queryset()), qs_repr)

    # TEMPLATE #
    def test_small_store_count_has_no_next_page(self):
        self.assertFalse(self.context['page_obj'].paginator.page(1).has_next())

    def test_large_store_count_has_next_page(self):
        for i in range(c.JSONSTORE_LIST_PAGINATE_BY + 1):
            f.JsonStoreFactory(user=self.test_user)
        self.setUp()
        self.assertTrue(self.context['page_obj'].paginator.page(1).has_next())
