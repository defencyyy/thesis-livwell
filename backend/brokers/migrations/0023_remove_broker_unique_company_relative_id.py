# Generated by Django 5.1.2 on 2024-12-17 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0022_alter_broker_relative_id_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='broker',
            name='unique_company_relative_id',
        ),
    ]
