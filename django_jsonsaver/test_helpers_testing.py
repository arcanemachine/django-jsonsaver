from django.contrib.auth.decorators import login_required
from django.test import SimpleTestCase
from unittest.mock import Mock

from . import helpers_testing as ht


class SetUpTestCaseMixinTest(SimpleTestCase):
    # METHODS #

    # get_response()
    def test_method_get_response_with_test_url(self):
        self.client = Mock()
        self.client.get = Mock(return_value='ok')
        self.assertEqual(
            ht.SetUpTestCaseMixin.get_response(self, True), 'ok')

    def test_method_get_response_no_test_url(self):
        self.test_url = 'ok'
        self.client = Mock()
        self.client.get = Mock(return_value=self.test_url)
        self.assertEqual(
            ht.SetUpTestCaseMixin.get_response(self, None), 'ok')

    # setUp()
    def test_method_setUp_auth_true_status_code_200(self):
        self.client = Mock()
        self.test_user = Mock()
        self.test_user.username = None
        self.client.login = Mock(return_value='ok')

        self.response = Mock()
        self.response.status_code = 200
        self.response.context = {'view': 'ok'}

        self.response.content = Mock()
        self.response.content.decode = Mock(return_value='ok')

        unescape = Mock(return_value='ok')  # noqa: F841

        self.get_response = Mock(return_value=self.response)

        ht.SetUpTestCaseMixin.setUp(self, True)
        self.assertEqual(self.context, {'view': 'ok'})
        self.assertEqual(self.html, 'ok')
        self.assertEqual(self.view_instance, 'ok')

    def test_method_setUp_auth_true_status_code_not_200(self):
        self.client = Mock()
        self.test_user = Mock()
        self.test_user.username = None
        self.client.login = Mock(return_value='ok')

        self.response = Mock()
        self.response.status_code = 'not 200'

        self.get_response = Mock(return_value=self.response)

        ht.SetUpTestCaseMixin.setUp(self, True)
        self.assertEqual(self.context, None)
        self.assertEqual(self.html, None)
        self.assertEqual(self.view_instance, None)

    def test_method_setUp_auth_false(self):
        self.client = Mock()
        self.client.logout = Mock(return_value='ok')

        self.get_response = Mock(return_value='ok')

        ht.SetUpTestCaseMixin.setUp(self, False)
        self.assertEqual(self.response, 'ok')
        self.assertEqual(self.client_logged_out, 'ok')


class GetFunctionArgsTest(SimpleTestCase):
    def test_get_function_args(self):

        def dummy_function(a, b, c):
            pass

        result = ht.get_function_args(dummy_function)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], 'a')
        self.assertEqual(result[1], 'b')
        self.assertEqual(result[2], 'c')


class GetFunctionDecoratorsTest(SimpleTestCase):
    def test_get_function_decorators(self):

        @login_required
        def dummy_function():
            pass

        result = ht.get_function_decorators(dummy_function)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], '@login_required')
