# Generated by Django 5.0.7 on 2024-10-04 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0003_alter_broker_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
