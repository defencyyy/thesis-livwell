# Generated by Django 5.1.2 on 2024-11-21 13:30

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brokers', '0015_alter_broker_email_alter_broker_password'),
        ('customers', '0007_customer_company'),
        ('units', '0014_merge_20241115_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_plan', models.CharField(max_length=255)),
                ('spot_discount_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tlp_discount_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('other_charges_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('spot_downpayment_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('reservation_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spread_downpayment_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payable_months', models.IntegerField()),
                ('payable_per_month', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_upon_turnover', models.DecimalField(decimal_places=2, max_digits=12)),
                ('net_unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount_payable', models.DecimalField(decimal_places=2, max_digits=12)),
                ('net_full_payment', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('broker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='brokers.broker')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='units.unit')),
            ],
        ),
    ]
