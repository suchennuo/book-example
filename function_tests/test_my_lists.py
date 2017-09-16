from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionTest
User = get_user_model()


#
class MyListsTest(FunctionTest):
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # 第一次访问domain， 设置一个 cookie
        # 加载 404 页面是最快的方式
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'yongchao1122@126.com'
        item1 = 'Right from the start'
        item2 = 'it was a faulty'
        item3 = 'put it right'
        # 登录
        self.create_pre_authenticated_session(email)

        # 进入主页，添加 lists
        self.browser.get(self.live_server_url)
        self.add_list_item(item1)
        self.add_list_item(item2)
        first_list_url = self.browser.current_url

        # 第一次看见 My lists 按钮
        self.browser.find_element_by_link_text('My lists').click()

        # 看见自己的 lists, 以第一条 list 为名
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(item1)
        )
        self.browser.find_element_by_link_text(item1).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # 添加新的 list
        self.browser.get(self.live_server_url)
        self.add_list_item(item3)
        second_list_url = self.browser.current_url

        # 在 my lists 页面中，出现新添加的 item
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text(item3)
        )
        self.browser.find_element_by_link_text(item3).click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text('My lists'),
                []
            )
        )
