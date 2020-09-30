# -*- coding: utf-8 -*-
"""
Module for testing article app views.
"""

import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from article.models import Article, Source, Category
from article.serializers import ArticleSerializer, ArticleListSerializer, SourceSerializer

from article.tests.test_models import create_demo_data


class SourceAPITest(TestCase):
    """Testing getting all sources"""

    def setUp(self):
        self.client = APIClient()

        create_demo_data()

        self.admin_user = User.objects.get(username='admin')
        self.admin_token = Token.objects.create(user=self.admin_user)

        self.my_source = Source.objects.create(
            name='Lenta',
            label='LNT',
            url='https://lenta.ru/',
        )

        self.my_category = Category.objects.create(
            name='Demo Cat',
        )

        self.valid_source = {
            'name': 'GazetaRU',
            'label': 'GZT',
            'url': 'https://gazeta.ru/',
            'categories': [self.my_category.pk, ]
        }
        self.invalid_source = {
            'name': 'GazetaRU2',
            'label': 'GZT2',
        }

    def test_get_all_sources(self):
        response = self.client.get(reverse('article:source-list'))
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_source(self):
        response = self.client.get(reverse('article:source-detail', args=[self.my_source.pk]))
        source = Source.objects.get(pk=self.my_source.pk)
        serializer = SourceSerializer(source)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_source(self):
        response = self.client.get(reverse('article:source-detail', args=[0]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_source(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.admin_token.key))
        response = self.client.post(
            reverse('article:source-list'),
            data=json.dumps(self.valid_source),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_source(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.admin_token.key))
        response = self.client.post(
            reverse('article:source-list'),
            data=json.dumps(self.invalid_source),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
