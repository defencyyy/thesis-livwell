# Generated by Django 5.0.7 on 2024-10-31 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_alter_company_logo_alter_company_name'),
        ('customers', '0006_remove_customer_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='companies.company'),
            preserve_default=False,
        ),
    ]
