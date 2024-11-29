# Generated by Django 5.1.2 on 2024-11-27 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_remove_document_is_verified_remove_document_name_and_more'),
        ('sales', '0008_alter_sale_status'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='document',
            name='documents_d_content_ba3031_idx',
        ),
        migrations.RemoveField(
            model_name='document',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='document',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='document',
            name='sale',
        ),
        migrations.AddField(
            model_name='document',
            name='sales',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='sales.sale'),
        ),
    ]
