# Generated by Django 5.0.7 on 2024-10-25 03:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brokers', '0008_alter_broker_name'),
        ('customers', '0005_remove_customer_date_sold_remove_customer_units'),
        ('sites', '0005_site_created_at_alter_site_picture'),
        ('units', '0007_remove_unit_sold_by_broker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sold', models.DateField(auto_now_add=True)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brokers.broker')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.unit')),
            ],
        ),
    ]
