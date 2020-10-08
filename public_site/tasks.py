# -*- coding: utf-8 -*-
"""Celery tasks goes here."""

from time import sleep

from my_smart_news.celery import app


@app.task(name='my_first_task')
def my_first_task():
    with open('celery_debug.log', 'a') as cel_file:
        cel_file.write('\nYO!')
    sleep(5)
    with open('celery_debug.log', 'a') as cel_file:
        cel_file.write('\ngoodbye!')

    return True
