# Generated by Django 5.1.2 on 2024-12-19 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0022_site_relative_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='relative_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
