# -*- coding: utf-8 -*-
"""
https://shazoo.ru/ parser.
"""

import concurrent.futures
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from time import sleep
from datetime import datetime

from my_smart_news.settings import logger
from smart_parser.helpers import extend_articles
from article.models import Article


class Shazoo:
    def __init__(self, driver):
        self.driver = driver

    def test_connection(self):
        """Test if Selenium successfully connected to feed."""

        auth_flag = False
        nav_logo = self.driver.find_element_by_class_name('navLogo')
        if nav_logo:
            try:
                logo_link = nav_logo.find_element_by_tag_name('a')
                if logo_link.get_attribute('href') == 'https://shazoo.ru/':
                    auth_flag = True
            except NoSuchElementException:
                logger.error('Can\'t find a tag inside Shazoo logo.')

        return auth_flag

    def do_parse(self, feed_url):
        """Start parsing process. Get pages to parse. Return generator with parsed articles"""

        articles = list()
        try:
            articles_added = extend_articles(articles, self.parse_page(feed_url))
            page = 1
            while articles_added:
                sleep(0.5)  # simulation user behavior
                page += 1
                articles_added = extend_articles(articles, self.parse_page('{}?page={}'.format(feed_url, page)))
        except Exception as ex:
            logger.error('Error during parsing process of feed: {}. Error: {}'.format(feed_url, ex))
        finally:
            self.driver.close()

        return articles

    def parse_page(self, page):
        """Receives page url to parse articles from. Returns list of articles."""

        self.driver.get(page)
        articles = self.driver.find_elements_by_tag_name('article')

        page_articles = list()
        if articles:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                page_articles = executor.map(self.parse_article, articles)

        return page_articles

    def parse_article(self, article):
        parsed_article = dict()

        try:
            article_time = article.find_element_by_tag_name('time').get_attribute('datetime')
            article_time = datetime.fromisoformat(article_time)
            is_actual_article = True if article_time.date() == datetime.today().date() else False
        except NoSuchElementException:
            article_time = ''
            is_actual_article = False
            logger.error('Can\'t find time of the article with text: {}'.format(article.text))

        if is_actual_article:
            try:
                h2 = article.find_element_by_tag_name('h2').text
                h2_a = article.find_element_by_tag_name('h2').find_element_by_tag_name('a')
                href = h2_a.get_attribute('href')
            except NoSuchElementException:
                href = ''
                h2 = ''
                logger.error('Can\'t find h2 for article with text: {}'.format(article.text))

            if href:
                try:
                    article = Article.objects.get(url=href)
                except Article.DoesNotExist:
                    article = None

                if not article:
                    try:
                        sleep(0.5)  # simulation user behavior
                        detail = BeautifulSoup(requests.get(href).content, 'lxml')
                        body_post = detail.find('section', {'class': 'body'})
                        if body_post:
                            picture = None
                            img_wrapper = detail.find('div', {'class': 'entryImageContainer'})
                            if img_wrapper:
                                picture = img_wrapper.find('img').attrs['src'] if img_wrapper.find('img') else None

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


class ShazooBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **kwargs):
        driver = self.create_driver()
        return Shazoo(driver)

    def create_driver(self):
        useragent = UserAgent()
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', useragent.random)

        driver = webdriver.Firefox(profile)

        url = "https://shazoo.ru"
        driver.get(url)

        return driver
