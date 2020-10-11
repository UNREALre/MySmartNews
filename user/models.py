# -*- coding: utf-8 -*-
"""
User related models goes here.
"""

from django.db import models
from django.contrib.auth.models import User

from article.views import Source


class UserSource(models.Model):
    """
    Sources that user select to read
    """

    user = models.ForeignKey(User, related_name='sources', on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
