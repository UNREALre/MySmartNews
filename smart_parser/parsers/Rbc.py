# -*- coding: utf-8 -*-
"""
https://rbc.ru/ parser.
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


class Rbc:
    def __init__(self, driver):
        self.driver = driver
        self.height = self.driver.execute_script("return document.body.scrollHeight")

    def test_connection(self):
        """Test if Selenium successfully connected to feed."""

        nav_logo = self.driver.find_element_by_class_name('topline__logo-block')
        auth_flag = True if nav_logo else False

        return auth_flag

    def height_change(self, locator):
        current_height = self.driver.execute_script("return document.body.scrollHeight")
        if current_height != self.height:
            self.height = current_height
            return True

        return False

    def do_parse(self, feed_url):
        """Start parsing process. Get pages to parse. Return generator with parsed articles"""

        self.driver.get(feed_url)

        # Simulation of scrolling down process, until all articles will be shown
        found_not_actual = False
        while True and not found_not_actual:
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.END)

            try:
                WebDriverWait(self.driver, 5).until(
                    self.height_change
                )
            except TimeoutException:
                break

            try:
                article_times = self.driver.find_elements_by_class_name('item__category')
                for times in article_times:
                    if len(times.text) > 5:  # actual is like "12:25"
                        found_not_actual = True
                        break
            except StaleElementReferenceException:
                logger.error('Time tag not found in articles feed from DTF source.')

        html_articles = self.driver.find_elements_by_class_name('js-category-item')
        articles = list()
        if html_articles:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                articles = executor.map(self.parse_article, html_articles)

        self.driver.close()

        return articles

    def parse_article(self, article):
        parsed_article = dict()

        try:
            article_stamp = article.find_element_by_class_name('item__category').text
            is_actual_article = True if len(article_stamp) == 5 else False
            if is_actual_article:
                article_time = datetime.now(pytz.timezone('Europe/Moscow'))
                article_time.replace(minute=int(article_stamp[3:]), hour=int(article_stamp[:2]))
        except NoSuchElementException:
            article_time = ''
            is_actual_article = False
            logger.error('Can\'t find time of the article with text: {}'.format(article.text))

        if is_actual_article:
            try:
                h2 = article.find_element_by_class_name('item__title').text
            except NoSuchElementException:
                h2 = ''
                logger.error('Can\'t find h2 for article with text: {}'.format(article.text))

            try:
                a_tag = article.find_element_by_class_name('item__link')
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
                        body_post = detail.find('div', {'class': 'l-col-main'})
                        if body_post:
                            # remove some web page stuff
                            try:
                                body_post = clean_page(body_post, {
                                    'div': [
                                        'article__header',
                                        'article__inline-video',
                                        'article__inline-item__link',
                                        'article__inline - item__category',
                                        'article__inline-item',
                                        'pro-anons',
                                        'article__authors',
                                        'article__tags',
                                        'banner',
                                        'banner__median_mobile',
                                        'article__main-image',
                                    ]
                                })
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


class RbcBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        driver = self.create_driver()
        return Rbc(driver)

    def create_driver(self):
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', useragent.random)

        driver = webdriver.Firefox(profile)

        url = "https://www.rbc.ru/"
        driver.get(url)

        return driver
