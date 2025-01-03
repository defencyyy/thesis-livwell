# Generated by Django 5.1.2 on 2024-11-29 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0018_alter_broker_username'),
        ('customers', '0010_alter_customer_customer_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='customer',
            unique_together={('broker', 'customer_code')},
        ),
    ]
