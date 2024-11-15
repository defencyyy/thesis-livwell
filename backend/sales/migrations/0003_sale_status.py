# Generated by Django 5.1.2 on 2024-11-11 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sale_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('under review', 'under review'), ('sold', 'Sold')], default='pending', max_length=20),
        ),
    ]
