# Generated by Django 2.0.6 on 2018-06-06 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=200)),
                ('article_text', models.TextField()),
                ('article_date', models.DateTimeField(auto_now_add=True)),
                ('article_modify_date', models.DateTimeField(auto_now_add=True)),
                ('article_pageviews', models.IntegerField(default=0)),
                ('article_ding', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=200)),
                ('class_article', models.ManyToManyField(to='blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_setting', models.CharField(blank=True, max_length=1024, null=True)),
                ('index_head_color', models.CharField(default='#545454', max_length=10)),
                ('index_notice', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=1024)),
                ('user_passwd', models.CharField(max_length=1024)),
                ('user_head', models.CharField(max_length=1024)),
                ('user_article', models.ManyToManyField(to='blog.Article')),
                ('user_article_class', models.ManyToManyField(to='blog.ArticleClass')),
            ],
        ),
        migrations.CreateModel(
            name='UserSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_name', models.CharField(max_length=30)),
                ('blog_info', models.CharField(default='怕是个肥狗子哦！', max_length=80)),
                ('blog_head_color', models.CharField(default='#545454', max_length=10)),
                ('blog_bgm', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.UserSite'),
        ),
    ]
