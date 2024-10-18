# Generated by Django 5.0.7 on 2024-10-04 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0003_alter_unit_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='unit',
            name='view',
            field=models.CharField(blank=True, choices=[('south', 'South'), ('north', 'North'), ('east', 'East'), ('west', 'West')], max_length=10),
        ),
    ]