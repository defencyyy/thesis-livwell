# Generated by Django 5.1.2 on 2024-12-13 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0019_site_address_alter_site_barangay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='other_charges',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='reservation_fee',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='spot_discount_flat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='spot_discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
