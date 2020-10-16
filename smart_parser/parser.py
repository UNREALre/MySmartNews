# -*- coding: utf-8 -*-
"""
Main parsing logic goes here. Parser starts his work here.
"""

from my_smart_news.settings import logger

from article.models import Article, Source
from smart_parser.factory import factory


@logger.catch
def start_parsing(source=None):
    """Fires parsing process."""

    if source is None:
        sources = Source.objects.all()
    else:
        sources = Source.objects.filter(label=source)

    for source in sources:
        with factory.create(source.label) as parser:
            if parser and parser.test_connection():
                logger.info('Successfully connected to source {}'.format(source.name))

                articles = parser.do_parse(source.url)
                save_to_db(articles, source)
            else:
                logger.error('Can\'t connect to source {}!'.format(source.name))


@logger.catch
def save_to_db(articles, source):
    """Save parsed articles to database"""

    for article in articles:
        if article and article.get('header'):
            article = Article(
                source=source,
                url=article.get('url'),
                header=article.get('header'),
                picture=article.get('picture'),
                text=article.get('text'),
                date=article.get('date'),
            )
            article.save()

            logger.info('Created new article {} with url: {}'.format(article.id, article.url))
