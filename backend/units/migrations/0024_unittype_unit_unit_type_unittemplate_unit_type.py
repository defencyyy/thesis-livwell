import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('units', '0023_unittemplate_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_custom', models.BooleanField(default=True)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='unit',
            name='unit_type',
            field=models.ForeignKey(
                null=True,  # Allow null values temporarily
                help_text='Type of the Unit (e.g., Studio, 1 Bedroom, etc.)',
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='units',
                to='units.unittype'
            ),
        ),
        migrations.AddField(
            model_name='unittemplate',
            name='unit_type',
            field=models.ForeignKey(
                null=True,  # Allow null values temporarily
                help_text='Type of the Unit (e.g., Studio, 1 Bedroom, etc.)',
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='unit_templates',
                to='units.unittype'
            ),
        ),
    ]
