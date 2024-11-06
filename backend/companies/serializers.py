# serializers.py
from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'description', 'logo', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['name', 'created_at', 'updated_at', 'is_active']

    def validate_logo(self, value):
        max_size = 5 * 1024 * 1024  
        if value.size > max_size:
            raise serializers.ValidationError("Logo file size must be less than 5 MB.")

        valid_mime_types = ['image/jpeg', 'image/png']
        if value.content_type not in valid_mime_types:
            raise serializers.ValidationError("Logo file type must be PNG, JPG, or JPEG.")

        return value
