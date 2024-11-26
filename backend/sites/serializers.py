from rest_framework import serializers
from .models import Site

class SiteSerializer(serializers.ModelSerializer):
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
        """Optional: Ensure the picture file is not too large."""
        max_size = 5 * 1024 * 1024  # 5 MB max size
        if value.size > max_size:
            raise serializers.ValidationError("The picture file is too large. Maximum size is 5MB.")
        return value
