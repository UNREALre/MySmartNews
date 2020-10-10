# -*- coding: utf-8 -*-
"""
Base top-level functional testing goes here, from the user point of view.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_load_homepage(self):
        # Visitor goes to the homepage of the web site
        self.browser.get(self.live_server_url)

        # Visitor gets page with correct page titlePage Title
        self.assertIn('My Smart News - новости, которые выбираете Вы!', self.browser.title)

        # Visitor passing the test for our system to find out his interests
        # ...
