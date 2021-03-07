from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AnonymousUser
from django.urls import resolve, reverse
from django.test import RequestFactory, SimpleTestCase


class UsersRootViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:users_root'), '/users/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/users/').view_name, 'users:users_root')


class UserRegisterViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:register'), '/users/register/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/register/').view_name, 'users:register')


class UserActivateRootUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_activate_root'), '/users/activate/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/activate/').view_name, 'users:user_activate_root')


class UserActivationEmailResendViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_activation_email_resend'),
            '/users/activate/resend-email/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/activate/resend-email/').view_name,
            'users:user_activation_email_resend')


class UserActivateViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_activate',
                    kwargs={'activation_code': 'test'}),
            '/users/activate/test/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/activate/test/').view_name, 'users:user_activate')


class UserLoginViewUrlTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:login'), '/users/login/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/login/').view_name, 'users:login')


class UserUsernameRecoverViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_username_recover'),
            '/users/login/forgot-username/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/login/forgot-username/').view_name,
            'users:user_username_recover')


class PasswordResetViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:password_reset'), '/users/login/forgot-password/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/login/forgot-password/').view_name,
            'users:password_reset')


class UserLogoutViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:logout'), '/users/logout/')

    def test_url_resolve(self):
        self.assertEqual(resolve('/users/logout/').view_name, 'users:logout')


class UserDetailMeViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:user_detail_me'), '/users/me/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/').view_name, 'users:user_detail_me')


class UserDetailPublicViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:user_detail_public', kwargs={
            'username': 'test'}), '/users/public/test/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/public/test/').view_name,
            'users:user_detail_public')


class UserUpdateTemplateViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(reverse('users:user_update'), '/users/me/settings/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/').view_name, 'users:user_update')


class UserUpdateAccountTierViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_update_account_tier'),
            '/users/me/settings/account-upgrade/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/account-upgrade/').view_name,
            'users:user_update_account_tier')


class UserUpdateEmailViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_update_email'), '/users/me/settings/email/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/email/').view_name,
            'users:user_update_email')


class UserUpdateEmailConfirmTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_update_email_confirm', kwargs={
                'activation_code': 'test'}), '/users/me/settings/email/test/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/email/test/').view_name,
            'users:user_update_email_confirm')


class PasswordChangeViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:password_change'),
            '/users/me/settings/password/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/password/').view_name,
            'users:password_change')


class UserUpdateIsPublicViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_update_is_public'),
            '/users/me/settings/profile-visibility/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/settings/profile-visibility/').view_name,
            'users:user_update_is_public')


class UserUpdateApiKeyViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_update_api_key'),
            '/users/me/renew-api-key/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/renew-api-key/').view_name,
            'users:user_update_api_key')


class UserDeleteViewTest(SimpleTestCase):
    def test_url_reverse(self):
        self.assertEqual(
            reverse('users:user_delete'),
            '/users/me/delete-account/')

    def test_url_resolve(self):
        self.assertEqual(
            resolve('/users/me/delete-account/').view_name,
            'users:user_delete')
