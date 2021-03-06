from django.test import TestCase
import accounts.views
from unittest.mock import Mock
from unittest.mock import patch, call
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email':'yongchao1122@126.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):

        self.client.post('/accounts/send_login_email', data={
            'email':'yongchao1122@126.com'
        })
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, '550906133@qq.com')
        self.assertEqual(to_list, ['yongchao1122@126.com'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'yongchao1122@126.com'
        }, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message,
                         "Check your email, we've sent you a link you can use to log in.")
        self.assertEqual(message.tags, "success")


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.post('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    #It is fairly straightforward.
    def test_creates_token_associated_with_email(self, mock_auth):
        self.client.post('/accounts/send_login_email', data={
            'email':'yongchao1122@126.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'yongchao1122@126.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail, mock_auth):
        self.client.post('/accounts/send_login_email', data={
            'email':'yongchao1122@126.com'
        })
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_email), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )
    # None != call(<WSGIRequest: GET '/account/login?...'>) 没有调用 auth.login.

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(mock_auth.login.called, False)

"""
self 可以这样用？在 fake_send_mail function 域外声明，赋值？
"""
