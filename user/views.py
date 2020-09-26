# -*- coding: utf-8 -*-
"""
This module contains all views for the user app
"""

from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User

from .serializers import UserSerializer


class UserCreate(CreateAPIView):
    """View for create user API"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class UserUpdate(UpdateAPIView):
    """View for update user API"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
