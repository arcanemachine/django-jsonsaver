import factory

from django.contrib.auth import get_user_model

from django_jsonsaver import constants as c
from stores.models import JsonStore
# from users.models import Profile

UserModel = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Usage:
        - Create object and save: e.g. user = UserFactory()
        - Build object but don't save: e.g. user = UserFactory.build()
    """
    class Meta:
        model = UserModel

    username = factory.Sequence(lambda n: f'{c.TEST_USER_USERNAME}_{n+1}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.PostGenerationMethodCall(
        'set_password', c.TEST_USER_PASSWORD)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    is_staff = False
    is_active = True
    last_login = None


class JsonStoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JsonStore

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'{c.TEST_JSONSTORE_NAME}_{n+1}')
    data = c.TEST_JSONSTORE_DATA
    is_public = False
