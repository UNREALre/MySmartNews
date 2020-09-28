# -*- coding: utf-8 -*-
"""
Article models: Sources, Categories, Articles, etc.
"""

from django.db import models


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

    Name - user friendly source name.
    Label - short name for system usage.
    URL - exact url of the source that will be parsed
    """

    name = models.CharField(max_length=255)
    label = models.CharField(max_length=100)
    url = models.URLField()
    categories = models.ManyToManyField(Category, related_name='sources')

    def __str__(self):
        return '#{} - {}'.format(self.id, self.name)
