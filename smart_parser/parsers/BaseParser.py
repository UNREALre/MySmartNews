# -*- coding: utf-8 -*-
"""
Base parser class with implementation of common methods for all other parsers to be inherited
"""

from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from django.conf import settings

from my_smart_news.settings import logger


class BaseParser:
    def __init__(self, driver):
        self.driver = driver
        self.height = self.driver.execute_script("return document.body.scrollHeight")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('exiting...')
        self.driver.close()
        return True  # Suppressing exception to continue parsing process for next sources

    def height_change(self, locator):
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        if current_height != self.height:
            self.height = current_height
            return True

        return False


class BaseBuilder:
    def __init__(self):
        self._instance = None

    def create_driver(self):
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', useragent.random)

        options = Options()
        options.headless = settings.BROWSER_HEADLESS

        binary = FirefoxBinary(settings.BROWSER_BINARY_PATH) if settings.BROWSER_BINARY_PATH else None

        driver = webdriver.Firefox(profile, options=options, firefox_binary=binary)

        return driver
