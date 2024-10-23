# Generated by Django 5.0.7 on 2024-10-04 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliations', '0003_remove_affiliation_is_active'),
        ('companies', '0003_alter_company_options_alter_company_logo'),
        ('sites', '0002_site_delete_building'),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('floor_area', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('lot_area', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('available', 'Available'), ('sold', 'Sold')], max_length=50)),
                ('affiliations', models.ManyToManyField(related_name='units', to='affiliations.affiliation')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='companies.company')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='sites.site')),
            ],
        ),
        migrations.DeleteModel(
            name='Units',
        ),
    ]
