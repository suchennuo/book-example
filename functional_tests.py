#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')
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
        inputbox.send_keys(Keys.ENTER)

        # inputbox = self.browser.find_element_by_id('id_new_item')
        # inputbox.send_keys('Use peacok feather t0 make a fly.')
        # inputbox.send_keys(Keys.ENTER)

        # table = self.browser.find_element_by_id('id_list_table')
        # #find_element_by_id
        #
        # rows = table.find_elements_by_tag_name('tr')
        # #find_elements_by_tag_name
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),
        #     "New to-do item did not appear in table -- its text was:\n%s" % (table.text)
        # )

        self.check_for_row_in_list_table('Buy peacock feathers')
        # self.check_for_row_in_list_table('Use peacok feather t0 make a fly.')

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')