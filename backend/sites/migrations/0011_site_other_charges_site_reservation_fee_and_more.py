# Generated by Django 5.1.2 on 2024-11-28 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0010_rename_city_site_municipality'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='other_charges',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='reservation_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='spot_discount_flat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='spot_discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='vat_percentage',
            field=models.DecimalField(decimal_places=2, default=12.0, max_digits=5),
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.PositiveIntegerField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floors', to='sites.site')),
            ],
        ),
    ]
