# Generated by Django 4.0.5 on 2022-06-22 08:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_article_end_article'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='end_article',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 29, 8, 49, 43, 654910, tzinfo=utc)),
        ),
    ]
