# Generated by Django 4.0.5 on 2022-06-21 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_created_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='author',
            new_name='seller',
        ),
    ]