# Generated by Django 5.0.7 on 2024-10-18 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0003_alter_company_options_alter_company_logo'),
        ('customers', '0003_remove_customer_description_customer_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='documents/')),
                ('is_verified', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='companies.company')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='customers.customer')),
            ],
        ),
    ]
