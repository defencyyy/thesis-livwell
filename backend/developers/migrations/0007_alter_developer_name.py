# Generated by Django 5.1.2 on 2024-10-24 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developers', '0006_alter_developer_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developer',
            name='name',
            field=models.CharField(editable=False, max_length=200),
        ),
    ]
