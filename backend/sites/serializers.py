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
            'location',
            'picture',
            'status',
            'created_at',
            'archived',  
        ]

        read_only_fields = ['id', 'created_at']  # These fields will be read-only

    def validate_status(self, value):
        """Ensure the status is within the allowed choices."""
        valid_statuses = [choice[0] for choice in Site.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status '{value}'. Allowed statuses are: {', '.join(valid_statuses)}.")
        return value
