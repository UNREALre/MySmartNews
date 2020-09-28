# -*- coding: utf-8 -*-
"""
This module contains all views for the article app.
"""

from rest_framework import permissions, viewsets

from .models import Source
from .serializers import SourceSerializer


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
