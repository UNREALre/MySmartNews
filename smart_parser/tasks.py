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


@logger.catch
@app.task(name='old_cleaner_task')
def old_cleaner_task():
    logger.info('Cleaning process started ... ')
    last_date = datetime.today() - timedelta(2)
    result = Article.objects.filter(date__lt=last_date).delete()
    logger.info('Cleaning completed. Deleted info: {}'.format(result))

    return True


@logger.catch
@app.task(name='main_parse_process_task')
def main_parse_process_task():
    logger.info('Starting parsing process ... ')
    start_parsing()
    logger.info('Parsing completed!')


@logger.catch
@app.task(name='celery_health_checker')
def celery_health_checker():
    logger.info('CLR_OK')
