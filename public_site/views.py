# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_smart_news.settings import logger


@logger.catch
def home_page(request):
    return render(request, 'index.html')
