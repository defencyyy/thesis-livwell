# Generated by Django 5.1.2 on 2024-11-26 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0009_remove_site_location_site_barangay_site_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='city',
            new_name='municipality',
        ),
    ]
