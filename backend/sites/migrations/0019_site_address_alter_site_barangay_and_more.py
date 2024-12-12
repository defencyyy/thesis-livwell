# Generated by Django 5.1.2 on 2024-12-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0018_site_numbering_type_site_section_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='address',
            field=models.CharField(blank=True, help_text='Optional additional address details (e.g., landmark, building, floor)', max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='barangay',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='maximum_months',
            field=models.PositiveIntegerField(default=60, help_text='Maximum months for downpayment (e.g., 60 months for 5 years max)'),
        ),
    ]
