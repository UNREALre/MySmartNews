# -*- coding: utf-8 -*-
"""
User Forms goes here
"""

from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(label=_('Запомнить меня'), required=False)
    # email = forms.EmailField(label=_('E-mail'), required=False)
