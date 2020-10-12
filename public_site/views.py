# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from my_smart_news.settings import logger
from article.models import Source, Article


@logger.catch
@login_required
@require_http_methods(['GET', 'POST'])
def home_page(request):

    user_sources = request.user.sources.all()
    articles = Article.objects.filter(source__in=user_sources).order_by('-date')
    paginator = Paginator(articles, 25)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_sources': user_sources,
        'page_obj': page_obj,
    }
    return render(request, 'index.html', context=context)


@logger.catch
@login_required
def manage_resources(request):
    if request.POST:
        source_id = int(request.POST['source'])
        status = request.POST['status']
        try:
            source = Source.objects.get(pk=source_id)
            ok = True
        except Source.DoesNotExist:
            ok = False
        else:
            if status == 'enable':
                request.user.sources.add(source)
            else:
                request.user.sources.remove(source)

        return JsonResponse({'ok': ok})
    else:
        user_sources = request.user.sources.order_by('name')
        all_sources = Source.objects.order_by('name')  # example of sorting, excessively ATM, cause of the Meta settings

        context = {
            'user_sources': user_sources,
            'all_sources': all_sources
        }
        return render(request, 'manage_source.html', context=context)
