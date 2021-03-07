import inspect

from html import unescape

from . import constants as c


class SetUpTestCaseMixin:
    def get_response(self, test_url=None):
        if test_url:
            return self.client.get(test_url)
        else:
            return self.client.get(self.test_url)

    def setUp(self, auth=True, test_url=None):
        if auth:
            self.client.login(username=self.test_user.username,
                              password=c.TEST_USER_PASSWORD)
            self.response = self.get_response(test_url)
            if self.response.status_code == 200:
                self.context = self.response.context
                self.html = unescape(self.response.content.decode('utf-8'))
                self.view_instance = self.response.context['view']
            else:
                self.context = self.html = self.view_instance = None
        else:
            self.client_logged_out = self.client.logout()
            self.response = self.get_response(test_url)


def get_function_args(f):
    """Returns list of args used in a given function"""
    return list(inspect.signature(f).parameters.keys())


def get_function_decorators(function):
    """Returns list of decorator names used in a given function"""
    source = inspect.getsource(function)
    index = source.find("def ")
    return [line.strip().split()[0]
            for line in source[:index].strip().splitlines()
            if line.strip()[0] == "@"]
