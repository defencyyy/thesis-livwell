# Generated by Django 5.1.2 on 2024-11-28 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0015_unittemplate_remove_unit_quantity_unit_other_charges_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='unit_template',
        ),
    ]