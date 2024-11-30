from rest_framework import serializers
from .models import Unit, UnitImage, UnitTemplate

class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ['id', 'unit', 'unit_template', 'image_type', 'image', 'uploaded_at']

class UnitTemplateSerializer(serializers.ModelSerializer):
    images = UnitImageSerializer(many=True)  # If you want to include images of the template

    class Meta:
        model = UnitTemplate
        fields = ['id', 'name', 'bedroom', 'bathroom', 'floor_area', 'lot_area', 'price', 'view', 'balcony', 'commission', 'images']

class UnitSerializer(serializers.ModelSerializer):
    images = UnitImageSerializer(many=True)  # If you want to include images of the unit

    class Meta:
        model = Unit
        fields = ['id', 'unit_number', 'unit_title', 'floor_area', 'lot_area', 'status', 'price', 'view', 'balcony', 'images']
