# Generated by Django 5.1.2 on 2024-10-24 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_rename_unit_customer_units_remove_customer_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_sold',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='units',
        ),
    ]
