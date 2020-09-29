# -*- coding: utf-8 -*-
"""
This module contains all serializers for the user app.
"""

from rest_framework import serializers

from .models import Source, Category, Article


class SourceSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Source
        fields = '__all__'
        depth = 1


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'header', 'text', 'url', 'date', 'source']
        depth = 1


class ArticleListSerializer(serializers.ModelSerializer):
    """Only for list of articles, return instead of full text - just a slice"""
    source_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'header', 'short_text', 'url', 'date', 'source_name']
        depth = 1

    def get_source_name(self, article):
        return article.source.name
