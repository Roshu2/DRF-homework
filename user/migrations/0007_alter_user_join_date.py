# Generated by Django 4.0.5 on 2022-06-17 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_userprofile_age_alter_userprofile_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='join_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='가입일'),
        ),
    ]
