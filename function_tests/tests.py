#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3) #隐式等待

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To_Do list', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        #find_element_by_tag_name

        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
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

        inputbox = self.browser.find_element_by_id('id_new_item')
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
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        job_list_url = self.browser.current_url
        self.assertRegex(job_list_url, '/lists/.+')
        self.assertNotEqual(job_list_url, edith_list_url)

        # 这个页面还是没有 aya 的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        self.fail('Finish the test!')
#
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')