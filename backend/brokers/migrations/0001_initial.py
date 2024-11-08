# Generated by Django 5.0.7 on 2024-10-02 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('affiliations', '0001_initial'),
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')),
                ('affiliations', models.ManyToManyField(related_name='brokers', to='affiliations.affiliation')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='companies.company')),
            ],
        ),
    ]
