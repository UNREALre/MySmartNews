# -*- coding: utf-8 -*-
"""
Parser tasks here. The list of tasks can be found below.

Scheduled tasks list:
1. One time per day at 02:00 remove all articles from the past day
2. Every 30 minutes parse all sources for article updates.
"""

from datetime import datetime, timedelta

from my_smart_news.celery import app
from my_smart_news.settings import logger
from article.models import Article
from smart_parser.parser import start_parsing


@app.task(name='old_cleaner_task')
def old_cleaner_task():
    logger.info('Cleaning process started ... ')
    yesterday = datetime.today() - timedelta(1)
    result = Article.objects.filter(date__lt=yesterday).delete()
    logger.info('Cleaning completed. Deleted info: {}'.format(result))

    return True


@app.task(name='main_parse_process_task')
def main_parse_process_task():
    logger.info('Starting parsing process ... ')
    start_parsing()
    logger.info('Parsing completed!')