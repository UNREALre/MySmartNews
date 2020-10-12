# -*- coding: utf-8 -*-
"""
https://echo.msk.ru/ parser.
"""

import concurrent.futures
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from time import sleep
from datetime import datetime
import pytz

from my_smart_news.settings import logger
from article.models import Article
from smart_parser.helpers import clean_page


class EchoMsk:
    def __init__(self, driver):
        self.driver = driver
        self.height = self.driver.execute_script("return document.body.scrollHeight")

    def test_connection(self):
        """Test if Selenium successfully connected to feed."""

        nav_logo = self.driver.find_element_by_class_name('logo')
        auth_flag = True if nav_logo else False

        return auth_flag

    def do_parse(self, feed_url):
        """Start parsing process. All actual articles here on one page. No need to load nothing more."""

        self.driver.get(feed_url)

        html_articles = self.driver.find_elements_by_class_name('newsblock')
        articles = list()
        if html_articles:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                articles = executor.map(self.parse_article, html_articles)

        self.driver.close()

        return articles

    def parse_article(self, article):
        parsed_article = dict()

        try:
            article_stamp = article.find_element_by_class_name('datetime').text
            article_time = datetime.now(pytz.timezone('Europe/Moscow'))
            article_time = article_time.replace(minute=int(article_stamp[3:]), hour=int(article_stamp[:2]))
        except NoSuchElementException:
            article_time = ''
            is_actual_article = False
            logger.error('Can\'t find time of the article with text: {}'.format(article.text))

        try:
            h2 = article.find_element_by_tag_name('h3').find_element_by_tag_name('a').text
        except NoSuchElementException:
            h2 = ''
            logger.error('Can\'t find h2 for article with text: {}'.format(article.text))

        try:
            a_tag = article.find_element_by_tag_name('h3').find_element_by_tag_name('a')
            href = a_tag.get_attribute('href')
        except NoSuchElementException:
            href = ''
            logger.error('Can\'t find a for article with text: {}'.format(article.text))

        if href:
            try:
                article = Article.objects.get(url=href)
            except Article.DoesNotExist:
                article = None

            if not article:
                try:
                    sleep(0.5)  # simulation user behavior
                    detail = BeautifulSoup(requests.get(href).content, 'lxml')
                    body_post = detail.find('div', {'class': 'typical'})
                    if body_post:
                        # remove some web page stuff
                        try:
                            if body_post.find('figure'):
                                body_post.find('figure').decompose()
                        except Exception as ex:
                            logger.error(
                                'Error "{}" while trying to remove unused elements from page: {}'.format(ex, href))

                        full_text = body_post.get_text().strip()
                        parsed_article = {
                            'url': href,
                            'header': h2,
                            'text': full_text,
                            'date': article_time,
                        }
                    else:
                        logger.error("URL {} has no body.".format(href))
                except Exception as ex:
                    logger.error('Error "{}" while trying to open url: {}'.format(ex, href))
            else:
                # we have already stored this article in database and just need to connect it with user
                parsed_article = {
                    'db_article': article
                }

        return parsed_article


class EchoMskBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        driver = self.create_driver()
        return EchoMsk(driver)

    def create_driver(self):
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', useragent.random)

        driver = webdriver.Firefox(profile)

        url = "https://echo.msk.ru/"
        driver.get(url)

        return driver
