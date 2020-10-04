# -*- coding: utf-8 -*-
"""
Class-command 'run'. Used to fire parsing process.

Example of call: python manage.py run
"""

from django.core.management.base import BaseCommand

from smart_parser.parser import start_parsing


class Command(BaseCommand):
    help = 'Starts parsing process'

    def handle(self, *args, **options):
        start_parsing()
