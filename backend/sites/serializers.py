from rest_framework import serializers
from .models import Site, Company

class SiteSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())  # Ensure company exists

    class Meta:
        model = Site
        fields = [
            'id',
            'company',
            'name',
            'description',
            'region',       
            'province',      
            'municipality',     
            'barangay',        
            'postal_code',     
            'picture',
            'status',
            'created_at',
            'archived',  
        ]
        read_only_fields = ['id', 'created_at']

    def validate_status(self, value):
        """Ensure the status is within the allowed choices."""
        valid_statuses = [choice[0] for choice in Site.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status '{value}'. Allowed statuses are: {', '.join(valid_statuses)}.")
        return value

    def validate_picture(self, value):
        """Optional: Ensure the picture file is not too large and is a valid image type."""
        if value:
            max_size = 5 * 1024 * 1024  # 5 MB max size
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            
            if value.size > max_size:
                raise serializers.ValidationError("The picture file is too large. Maximum size is 5MB.")
            
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(f"Invalid image type. Allowed types are: {', '.join(allowed_types)}.")
        return value

    def validate(self, data):
        """Additional validation for required fields (if they are not included in 'required' attribute)."""
        required_fields = ['name', 'region', 'province', 'municipality', 'barangay', 'status']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f"{field} is required and cannot be empty.")
        return data
