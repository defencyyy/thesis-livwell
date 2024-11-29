# Generated by Django 5.1.2 on 2024-11-28 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0016_remove_unit_unit_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='unit_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='units', to='units.unittemplate'),
        ),
    ]