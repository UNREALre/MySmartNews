# -*- coding: utf-8 -*-
"""
Helper-functions for different functionality inside application.
"""


def extend_articles(articles, new_articles):
    """Add parsed articles from page to article list and returns the number of newly added articles"""

    counter = 0
    for article in new_articles:
        if article:
            articles.append(article)
            counter += 1

    return counter


def clean_page(page, bad_elements):
    """Clean bs4 HTML from bad elements"""

    for tag, classes in bad_elements.items():
        for tag_class in classes:
            if page.find(tag, {'class': tag_class}):
                page.find(tag, {'class': tag_class}).decompose()

    return page
