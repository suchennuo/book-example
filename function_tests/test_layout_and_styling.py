#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
from .base import FunctionTest
import sys

class LayoutAndStylingTest(FunctionTest):

    def test_layout_and_styling(self):
        self.browser.get(self.server_ul)
        self.browser.set_window_size(1024, 786)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )