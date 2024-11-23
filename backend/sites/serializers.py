from rest_framework import serializers
from .models import Site

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = [
            'id',        # Include the ID for referencing
            'company',   # Foreign key to the company
            'name',      # Name of the site
            'description',  # Site description
            'location',  # Site location
            'picture',   # Picture URL or file path
            'status',    # Site status
            'created_at' # Date the site was created
        ]
        read_only_fields = ['id', 'created_at']  # These fields will be read-only
