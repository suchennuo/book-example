from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib import auth
from accounts.models import Token

User = get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='yongchao1122@126.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        user = User(email='yongchao1122@126.com')
        self.assertEqual(user.pk, 'yongchao1122@126.com')

    # should be able to link an email to a unique ID, and that
    #  UID shouldn't be the same two times in a row
    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='yongchao1122@126.com')
        token2 = Token.objects.create(email='yongchao1122@126.com')
        self.assertNotEqual(token1.uid, token2.uid)

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='yongchao1122@126.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)
