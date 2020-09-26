# -*- coding: utf-8 -*-
"""
This module contains all serializers for the user app.
"""

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
