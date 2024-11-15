# Generated by Django 5.1.2 on 2024-11-12 17:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developers', '0010_developer_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='contact_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message='Enter a valid phone number (9 to 15 digits).')]),
        ),
        migrations.AlterField(
            model_name='developer',
            name='password',
            field=models.CharField(default=12345, max_length=128),
            preserve_default=False,
        ),
    ]