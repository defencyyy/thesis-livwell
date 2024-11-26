# Generated by Django 5.1.2 on 2024-11-26 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0008_site_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='location',
        ),
        migrations.AddField(
            model_name='site',
            name='barangay',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='city',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='province',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='region',
            field=models.CharField(default=3, max_length=100),
            preserve_default=False,
        ),
    ]