# Generated by Django 5.1.2 on 2024-11-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0016_alter_broker_options_broker_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='broker',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]