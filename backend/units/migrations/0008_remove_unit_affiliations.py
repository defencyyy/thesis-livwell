# Generated by Django 5.1.2 on 2024-11-06 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0007_remove_unit_sold_by_broker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='affiliations',
        ),
    ]
