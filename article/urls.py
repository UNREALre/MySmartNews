# -*- coding: utf-8 -*-
"""
This module contains all url routes of the article app
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SourceViewSet

app_name = 'article'

router = DefaultRouter()
router.register(r'sources', SourceViewSet, basename='source')

urlpatterns = [
] + router.urls
