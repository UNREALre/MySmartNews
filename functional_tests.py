# -*- coding: utf-8 -*-
"""
Base top-level functional testing goes here.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

project_url = 'http://localhost:8000/'


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_load_homepage(self):
        # Visitor goes to the homepage of the web site
        self.browser.get(project_url)

        # Page Title check
        self.assertIn('Page not found at /', self.browser.title)

        # Visitor passing the test for our system to find out his interests
        # ...


if __name__ == '__main__':
    unittest.main()
