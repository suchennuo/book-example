#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
from .base import FunctionTest

import sys

class NewVisitorTest(FunctionTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_ul)
        self.assertIn('To-Do list', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        #find_element_by_tag_name

        self.assertIn('To-Do', header_text)

        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        inputbox.send_keys('Buy peacock feathers')
        #send_keys ， selenium 在输入框中输入内容的方法

        # aya 按回车， 被带到一个新的 URL
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacok feather to make a fly.')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，aya 的清单中显示了这两个待办事项
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacok feather to make a fly.')

        ## 使用一个新的浏览器 session， 确保 aya 的信息不会从 cookie 泄露
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Job 访问首页， 看不到 Aya 的清单内容
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Job 输入一个新的待办事项，新建一个清单
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        job_list_url = self.browser.current_url
        self.assertRegex(job_list_url, '/lists/.+')
        self.assertNotEqual(job_list_url, edith_list_url)

        # 这个页面还是没有 aya 的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # self.fail('Finish the test!')