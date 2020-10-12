# -*- coding: utf-8 -*-

from django.conf.urls import url
from public_site import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url('manage-sources/', views.manage_resources, name='manage-resources'),
]
