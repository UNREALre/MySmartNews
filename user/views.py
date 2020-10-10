# -*- coding: utf-8 -*-
"""
This module contains all views for the user app
"""

from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views import View
from django.shortcuts import render, redirect


from .serializers import UserSerializer
from user.forms import LoginForm


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


class CustomLoginView(LoginView):
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = UserCreationForm()

        context = {
            'form': form
        }

        return render(request, 'registration/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.email = request.POST['username']
            new_user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')

        context = {
            'form': form
        }

        return render(request, 'registration/signup.html', context)
