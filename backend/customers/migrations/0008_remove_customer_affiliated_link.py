# Generated by Django 5.1.2 on 2024-11-22 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_customer_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='affiliated_link',
        ),
    ]
