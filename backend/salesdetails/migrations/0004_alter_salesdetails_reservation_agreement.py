# Generated by Django 5.1.2 on 2024-11-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salesdetails', '0003_salesdetails_reservation_agreement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesdetails',
            name='reservation_agreement',
            field=models.FileField(blank=True, null=True, upload_to='reservations/'),
        ),
    ]
