# -*- coding: utf-8 -*-
"""
User related models goes here.
"""

from django.db import models
from django.contrib.auth.models import User

from article.models import Source


class UserSources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sources')
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    source_order = models.IntegerField()

    def __str__(self):
        return '#{}. {} - {}'.format(self.id, self.user.username, self.source.name)

    class Meta:
        ordering = [
            'source_order',
        ]
