# -*- coding: utf-8 -*-
"""
This module contains all views for the article app.
"""

from rest_framework import permissions, viewsets

from .models import Source, Article
from .serializers import SourceSerializer, ArticleSerializer, ArticleListSerializer


class SourcePermission(permissions.BasePermission):
    """Permissions for different API actions with sources"""

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return False


class SourceViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations with Sources"""

    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    permission_classes = [SourcePermission, ]


class ArticlePermission(permissions.BasePermission):
    """Permissions for different API actions with articles"""

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser
        else:
            return False


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations with Articles"""

    serializer_class = ArticleSerializer
    permission_classes = [ArticlePermission, ]

    def list(self, request, *args, **kwargs):
        """For list action API we have to change serializer"""
        self.serializer_class = ArticleListSerializer
        return super(ArticleViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        """Restricting queryset to contain only user related articles"""

        user = self.request.user
        queryset = Article.objects.all() if user.is_superuser else user.articles.all()
        return queryset

    def filter_queryset(self, queryset):
        queryset = super(ArticleViewSet, self).filter_queryset(queryset)
        return queryset.order_by('-date')
