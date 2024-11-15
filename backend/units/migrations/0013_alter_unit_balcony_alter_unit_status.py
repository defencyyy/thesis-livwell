# Generated by Django 5.1.2 on 2024-11-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0012_delete_unitimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='balcony',
            field=models.CharField(blank=True, choices=[('has balcony', 'Has Balcony'), ('no balcony', 'No Balcony')], max_length=20),
        ),
        migrations.AlterField(
            model_name='unit',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold', 'Sold'), ('pending reservation', 'Pending Reservation'), ('Reserved', 'Reserved')], max_length=50),
        ),
    ]
