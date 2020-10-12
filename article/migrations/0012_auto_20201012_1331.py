# Generated by Django 3.1.2 on 2020-10-12 09:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0011_auto_20201012_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='sources', to=settings.AUTH_USER_MODEL),
        ),
    ]
