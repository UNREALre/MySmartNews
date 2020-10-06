# -*- coding: utf-8 -*-
"""
Class-command 'run'. Used to fire parsing process.

Example of call: python manage.py run
"""

from django.core.management.base import BaseCommand

from smart_parser.parser import start_parsing


class Command(BaseCommand):
    help = 'Starts parsing process'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--source', type=str, help='if parser has to parse only one concrete source')

    def handle(self, *args, **options):
        source = options.get('source', None)
        start_parsing(source)
