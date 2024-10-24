# Generated by Django 5.1.2 on 2024-10-24 12:41

import django.utils.timezone
import sites.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0004_site_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=sites.models.logo_upload_path),
        ),
    ]
