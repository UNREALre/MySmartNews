# Generated by Django 3.1.2 on 2020-10-12 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_article_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='subscribers',
        ),
    ]
