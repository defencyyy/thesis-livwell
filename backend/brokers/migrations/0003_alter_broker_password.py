# Generated by Django 5.0.7 on 2024-10-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0002_broker_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broker',
            name='password',
            field=models.CharField(max_length=128, null=True),
        ),
    ]