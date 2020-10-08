# -*- coding: utf-8 -*-

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_smart_news.settings')
app = Celery('my_smart_news')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'parse-new-articles-once-per-30-mins': {
        'task': 'main_parse_process_task',
        'schedule': crontab(minute='*/15'),
    },
    'clean-old-art-once-per-day': {
        'task': 'old_cleaner_task',
        'schedule': crontab(hour=15, minute=30),
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
