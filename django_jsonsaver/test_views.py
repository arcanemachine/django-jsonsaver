from django.test import TestCase
from django.urls import reverse


class ProjectRootViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('project_root'))

    def test_get_method_unauthenticated_user(self):
        self.assertTrue(self.response.status_code, 200)

    def test_template_name(self):
        self.assertTemplateUsed(self.response, 'project_root.html')

    def test_view_function_name(self):
        self.assertEqual(
            self.response.resolver_match.view_name, 'project_root')
