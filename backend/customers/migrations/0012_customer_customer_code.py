# Generated by Django 5.1.2 on 2024-11-29 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0011_remove_customer_customer_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_code',
            field=models.CharField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]
