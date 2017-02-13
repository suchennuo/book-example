#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
import sys

class FunctionTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_ul = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_ul = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_ul == cls.live_server_url:
            super().tearDownClass()


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3) #隐式等待

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])