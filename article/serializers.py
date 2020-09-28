# -*- coding: utf-8 -*-
"""
This module contains all serializers for the user app.
"""

from rest_framework import serializers
from .models import Source, Category


class SourceSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Source
        fields = '__all__'
        depth = 1
