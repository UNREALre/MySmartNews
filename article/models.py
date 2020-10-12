# -*- coding: utf-8 -*-
"""
Article models: Sources, Categories, Articles, etc.
"""

import re
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Categories for Sources Model.

    Name - user friendly category name.
    """

    name = models.CharField(max_length=255)

    def __str__(self):
        return '#{} - {}'.format(self.id, self.name)


class Source(models.Model):
    """
    Source Model.

    name - user friendly source name.
    label - short name for system usage.
    url - exact url of the source that will be parsed
    """

    name = models.CharField(max_length=255)
    label = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='sources')
    subscribers = models.ManyToManyField(User, related_name='sources', blank=True)

    def __str__(self):
        return '#{}. {}'.format(self.id, self.name)

    class Meta:
        indexes = [
            models.Index(fields=['name', ]),
            models.Index(fields=['url', ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=['url', ], name='unique source url')
        ]
        ordering = [
            'name',
        ]


class Article(models.Model):
    """
    Article Model.

    header - parsed name of the article
    text - parsed full text of the article
    date - parsed date of the article
    date_added - when the article was added to DB
    url - url of the article
    source_id - id of the source
    """

    header = models.CharField(max_length=255)
    picture = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    url = models.URLField()
    date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    @property
    def short_text(self):
        """Returns short version of full-text"""

        clean_text = re.sub('[^A-Za-zа-яА-Я0-9 ]+', '', self.text)
        return clean_text[:500]

    def __str__(self):
        return '#{}. {}'.format(self.id, self.header)

    class Meta:
        """URL and header fields has to be indexed, because of many searches using them during parser process"""

        indexes = [
            models.Index(fields=['url', ]),
            models.Index(fields=['header', ]),
        ]
        constraints = [
            models.UniqueConstraint(fields=['url', ], name='unique article url')
        ]
