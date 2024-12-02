# Generated by Django 5.1.2 on 2024-12-02 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_alter_company_logo_alter_company_name'),
        ('units', '0022_alter_unit_floor'),
    ]

    operations = [
        migrations.AddField(
            model_name='unittemplate',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='companies.company'),
            preserve_default=False,
        ),
    ]