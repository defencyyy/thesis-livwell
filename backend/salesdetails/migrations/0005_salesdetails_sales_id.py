# Generated by Django 5.1.2 on 2024-12-06 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_merge_20241204_2258'),
        ('salesdetails', '0004_alter_salesdetails_reservation_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdetails',
            name='sales_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.sale'),
        ),
    ]