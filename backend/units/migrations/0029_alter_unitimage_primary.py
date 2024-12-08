from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0027_merge_20241207_1310'),
        ('units', '0028_merge_20241208_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitimage',
            name='primary',
            field=models.BooleanField(blank=True, default=False, help_text='Indicates if this image is the primary image for the template', null=True),
        ),
    ]
