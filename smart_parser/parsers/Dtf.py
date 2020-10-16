# -*- coding: utf-8 -*-
"""
https://dtf.ru/ parser.
"""

import concurrent.futures
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from datetime import datetime
import pytz

from my_smart_news.settings import logger
from article.models import Article
from smart_parser.helpers import clean_page
from smart_parser.parsers.BaseParser import BaseParser, BaseBuilder


class Dtf(BaseParser):
    def test_connection(self):
        """Test if Selenium successfully connected to feed."""

        nav_logo = self.driver.find_element_by_class_name('site-header__item--logo')
        auth_flag = True if nav_logo else False

        return auth_flag

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
                t_links = self.driver.find_elements_by_class_name('t-link')
                for link in t_links:
                    if 'вчера' in link.text:
                        found_not_actual = True
                        break
            except StaleElementReferenceException:
                logger.error('Time tag not found in articles feed from DTF source.')

        html_articles = self.driver.find_elements_by_class_name('feed__item')
        articles = list()

        if html_articles:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                articles = executor.map(self.parse_article, html_articles)

        return articles

    def parse_article(self, article):
        parsed_article = dict()

        try:
            article_stamp = int(article.find_element_by_tag_name('time').get_attribute('data-date'))
            article_time = datetime.fromtimestamp(article_stamp, pytz.timezone('Europe/Moscow'))
            is_actual_article = True if article_time.date() == datetime.today().date() else False
        except NoSuchElementException:
            article_time = ''
            is_actual_article = False
            logger.error('Can\'t find time of the article with text: {}'.format(article.text))

        if is_actual_article:
            try:
                h2 = article.find_element_by_tag_name('h2').text
            except NoSuchElementException:
                h2 = ''
                logger.error('Can\'t find h2 for article with text: {}'.format(article.text))

            try:
                a_tag = article.find_element_by_class_name('t-link')
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
                        body_post = detail.find('div', {'class': 'content--full'})
                        if body_post:
                            img_wrapper = detail.find('div', {'class': 'andropov_image'})
                            picture = img_wrapper.attrs['data-image-src'] if img_wrapper else None

                            # remove some web page stuff
                            try:
                                body_post = clean_page(body_post, {
                                    'div': [
                                        'content-counters',
                                        'authorCard',
                                    ]
                                })

                                if body_post.find('figure'):
                                    body_post.find('figure').decompose()
                            except Exception as ex:
                                logger.error(
                                    'Error "{}" while trying to remove unused elements from page: {}'.format(ex, href))

                            full_text = body_post.get_text().strip()
                            parsed_article = {
                                'url': href,
                                'header': h2,
                                'picture': picture,
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


class DtfBuilder(BaseBuilder):
    def __call__(self, **kwargs):
        driver = self.create_driver()
        driver.get("https://dtf.ru/")
        return Dtf(driver)
