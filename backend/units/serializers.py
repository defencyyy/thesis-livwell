from rest_framework import serializers
from .models import Unit, UnitImage, UnitTemplate, UnitType
from companies.models import Company

class UnitImageSerializer(serializers.ModelSerializer):
    # Ensure that we are serializing the correct relation based on image_type
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all(), required=False)
    unit_template = serializers.PrimaryKeyRelatedField(queryset=UnitTemplate.objects.all(), required=False)

    class Meta:
        model = UnitImage
        fields = '__all__'

    def validate(self, data):
        # Ensure that either 'unit' or 'unit_template' is provided depending on 'image_type'
        if data['image_type'] == 'unit' and not data.get('unit'):
            raise serializers.ValidationError("Unit must be set when the image type is 'unit'")
        if data['image_type'] == 'unit_template' and not data.get('unit_template'):
            raise serializers.ValidationError("Unit Template must be set when the image type is 'unit_template'")
        return data

class UnitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitType
        fields = '__all__'

class UnitTemplateSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())  # Add company field
    images = UnitImageSerializer(many=True, required=False)  # Allow images to be included during creation/update
    unit_type = serializers.PrimaryKeyRelatedField(queryset=UnitType.objects.all())

    class Meta:
        model = UnitTemplate
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        template = UnitTemplate.objects.create(**validated_data)

        # Handle image creation separately (if provided)
        if images_data:
            for image_data in images_data:
                image_data['unit_template'] = template  # Set the template reference
                UnitImage.objects.create(**image_data)

        return template

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)

        # Handle image updates separately (if provided)
        if images_data:
            # Delete old images
            instance.images.all().delete()
            # Create new images
            for image_data in images_data:
                image_data['unit_template'] = instance  # Set the template reference
                UnitImage.objects.create(**image_data)

        return instance

class UnitSerializer(serializers.ModelSerializer):
    images = UnitImageSerializer(many=True, required=False)

    class Meta:
        model = Unit
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        unit = Unit.objects.create(**validated_data)
        # Create UnitImage objects associated with this unit
        UnitImage.objects.bulk_create(
            [UnitImage(unit=unit, **image_data) for image_data in images_data]
        )
        return unit

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)
        if images_data:
            # Remove old images
            instance.images.all().delete()
            # Create new UnitImage objects for the updated unit
            UnitImage.objects.bulk_create(
                [UnitImage(unit=instance, **image_data) for image_data in images_data]
            )
        return instance
