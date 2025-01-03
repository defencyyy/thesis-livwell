# Generated by Django 5.1.2 on 2024-12-12 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0015_remove_floor_site_section'),
        ('units', '0034_rename_floor_unit_section_alter_unit_unit_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='sites.section'),
        ),
    ]
