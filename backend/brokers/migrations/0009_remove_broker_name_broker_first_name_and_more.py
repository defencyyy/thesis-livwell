# Generated by Django 5.1.2 on 2024-10-26 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brokers', '0008_alter_broker_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broker',
            name='name',
        ),
        migrations.AddField(
            model_name='broker',
            name='first_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='broker',
            name='last_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='broker',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
