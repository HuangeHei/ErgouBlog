# Generated by Django 2.0.6 on 2018-06-12 03:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_article_touxiang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='article_touxiang',
        ),
    ]
