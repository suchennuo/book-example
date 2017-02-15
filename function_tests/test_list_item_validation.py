#functional tests.
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
from .base import FunctionTest
from lists.forms import EMPTY_LIST_ERROR
import sys

class ItemValidationTest(FunctionTest):

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_ul)
        self.get_item_input_box().send_keys('\n')

        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        # error = self.browser.find_element_by_css_selector('.has-error')
        # self.assertEqual(error.text, "You can't have an empty list item")

        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')