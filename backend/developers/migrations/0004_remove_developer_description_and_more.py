# Generated by Django 5.1.2 on 2024-10-24 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('developers', '0003_developer_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='developer',
            name='description',
        ),
        migrations.RemoveField(
            model_name='developer',
            name='picture',
        ),
    ]
