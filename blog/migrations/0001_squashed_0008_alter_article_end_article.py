# Generated by Django 4.0.5 on 2022-06-21 02:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('blog', '0001_initial'), ('blog', '0002_comment'), ('blog', '0003_article_end_article_article_show_article'), ('blog', '0004_alter_article_end_article_alter_article_show_article'), ('blog', '0005_alter_article_end_article_alter_article_show_article'), ('blog', '0006_alter_article_end_article_alter_article_show_article'), ('blog', '0007_alter_article_end_article_alter_article_show_article'), ('blog', '0008_alter_article_end_article')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('content', models.TextField(max_length=255)),
                ('category', models.ManyToManyField(related_name='articles', to='blog.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('end_article', models.DateTimeField(default=datetime.datetime(2022, 6, 28, 1, 57, 53, 736708, tzinfo=utc))),
                ('show_article', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=256, verbose_name='댓글')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
