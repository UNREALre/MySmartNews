# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from my_smart_news.settings import logger
from article.models import Source, Article
from user.models import UserSources


@logger.catch
@login_required
@require_http_methods(['GET', 'POST'])
def home_page(request):

    user_sources = request.user.sources.all()
    articles = Article.objects.filter(source__usersources__in=user_sources).order_by('source__usersources__source_order')
    paginator = Paginator(articles, 50)

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
        source_order = request.POST['source_order']
        try:
            source = Source.objects.get(pk=source_id)
            ok = True
        except Source.DoesNotExist:
            ok = False
        else:
            if status == 'enable':
                try:
                    user_source = UserSources.objects.get(user=request.user, source=source)
                    user_source.source_order = source_order
                except UserSources.DoesNotExist:
                    user_source = UserSources(user=request.user, source=source, source_order=source_order)
                finally:
                    user_source.save()
            else:
                try:
                    UserSources.objects.get(user=request.user, source=source).delete()
                except UserSources.DoesNotExist:
                    logger.error('Trying to disable user ({}) source ({}) that is not in DB'.format(
                        request.user.username, source.name))

        return JsonResponse({'ok': ok})
    else:
        user_sources = request.user.sources.all()
        all_sources = Source.objects.order_by('usersources__source_order')

        context = {
            'user_sources': user_sources,
            'all_sources': all_sources
        }
        return render(request, 'manage_source.html', context=context)
