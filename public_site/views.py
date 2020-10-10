# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from my_smart_news.settings import logger


@logger.catch
@login_required
def home_page(request):
    context = {

    }
    return render(request, 'index.html', context=context)
