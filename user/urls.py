# -*- coding: utf-8 -*-
"""
This module contains all url routes of the app
"""

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreate, UserUpdate, CustomLoginView, SignUpView

app_name = 'user'

urlpatterns = [
    path('token/', obtain_auth_token, name='get_token'),
    path('create/', UserCreate.as_view(), name='create_user'),
    path('update/', UserUpdate.as_view(), name='update_user'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(success_url=reverse_lazy('user:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('user:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
