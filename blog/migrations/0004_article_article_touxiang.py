# Generated by Django 2.0.6 on 2018-06-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_article_article_is_save'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_touxiang',
            field=models.CharField(default='toux.jpg', max_length=200),
        ),
    ]
