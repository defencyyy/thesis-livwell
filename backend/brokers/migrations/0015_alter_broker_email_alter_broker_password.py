# Generated by Django 5.1.2 on 2024-11-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0014_alter_broker_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broker',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='broker',
            name='password',
            field=models.CharField(default=12345, max_length=128),
            preserve_default=False,
        ),
    ]
