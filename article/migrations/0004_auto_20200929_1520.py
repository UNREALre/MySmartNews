# Generated by Django 3.1.1 on 2020-09-29 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_users'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='article',
            constraint=models.UniqueConstraint(fields=('url',), name='unique source url'),
        ),
    ]