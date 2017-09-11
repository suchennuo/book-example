#functional tests.
from selenium import webdriver
import os
import unittest
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
import sys
MAX_WAIT = 10


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    return modified_fn



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

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_for(self, fn):
        return fn()











"""
10月8号，乘坐D2505, 11:08 从大荔站发车， 11:47 到西安北。
然后乘坐 G1282, 13:00 从西安北出发，19:15 到天津。

G674 17:30 到 23:00 到北京

"""