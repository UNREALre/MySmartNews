# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_smart_news.settings import logger

from .tasks import my_first_task


@logger.catch
def home_page(request):
    # my_first_task.delay()
    return render(request, 'index.html')
