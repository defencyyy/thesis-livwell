# Generated by Django 5.1.2 on 2024-12-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0013_site_maximum_months'),
    ]

    operations = [
        migrations.RenameField(
            model_name='floor',
            old_name='floor_number',
            new_name='number',
        ),
        migrations.AddField(
            model_name='floor',
            name='name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='maximum_months',
            field=models.PositiveIntegerField(default=60, help_text='Maximum months for payment term (e.g., 60 months for 5 years max)'),
        ),
    ]
