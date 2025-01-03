from django.db import migrations

def update_default_unit_types(apps, schema_editor):
    UnitType = apps.get_model('units', 'UnitType')

    # New default unit types
    new_default_unit_types = [
        'Studio', 
        '1 Bedroom', 
        '2 Bedroom', 
        '3 Bedroom', 
        'Penthouse', 
        'Loft', 
        'Townhouse',
        'Single Detached',
        'Single Attached',
        'Duplex',
        'Parking',
        'Bungalow',
    ]

    # Remove old default types that are no longer needed
    old_defaults_to_remove = [
        'Studio Deluxe'
    ]

    # Add new default unit types
    for unit_type in new_default_unit_types:
        UnitType.objects.get_or_create(
            name=unit_type,
            defaults={'is_custom': False}
        )

    # Delete old default types
    for unit_type in old_defaults_to_remove:
        UnitType.objects.filter(name=unit_type, is_custom=False).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('units', '0038_merge_20241215_1107'),
    ]

    operations = [
        migrations.RunPython(update_default_unit_types),
    ]
