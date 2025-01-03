# Generated by Django 5.1.2 on 2024-12-15 00:27

import django.db.models.deletion
import units.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_alter_company_logo_alter_company_name'),
        ('units', '0036_alter_unittemplate_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.ForeignKey(default=units.models.get_default_unit_type, help_text='Type of the Unit (e.g., Studio, 1 Bedroom, etc.)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='units', to='units.unittype'),
        ),
        migrations.AlterField(
            model_name='unittemplate',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='companies.company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unittemplate',
            name='unit_type',
            field=models.ForeignKey(default=units.models.get_default_unit_type, help_text='Type of the Unit (e.g., Studio, 1 Bedroom, etc.)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unit_templates', to='units.unittype'),
        ),
    ]
