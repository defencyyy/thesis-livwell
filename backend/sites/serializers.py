from rest_framework import serializers
from .models import Site, Company
from .models import Floor

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['id', 'floor_number']

class SiteSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())  # Ensure company exists
    floors = FloorSerializer(many=True, read_only=True)  # Add this line
    number_of_floors = serializers.IntegerField(write_only=True, required=False)  # New field to add floors

    class Meta:
        model = Site
        fields = [
            'id',
            'company',
            'picture',
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
            'floors',
            'number_of_floors',  # Include new field
            'total_units', 
            'location',
            'available_units',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Extract the number of floors
        number_of_floors = validated_data.pop('number_of_floors', 0)
        
        # Create the site
        site = super().create(validated_data)

        # Create floors based on the number_of_floors
        for i in range(1, number_of_floors + 1):
            Floor.objects.create(site=site, floor_number=i)

        return site

    def update(self, instance, validated_data):
        # Extract floors data from validated_data
        floors_data = validated_data.pop('floors', [])
        
        # Update fields of the site instance
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # Retrieve existing floors for the site
        existing_floors = {floor.floor_number: floor for floor in instance.floors.all()}
        
        # Keep track of processed floors to handle deletions later
        processed_floors = set()

        # Iterate through incoming floors data
        for floor_data in floors_data:
            floor_number = floor_data['floor_number']
            processed_floors.add(floor_number)

            if floor_number in existing_floors:
                # Update existing floor
                floor = existing_floors[floor_number]
                for key, value in floor_data.items():
                    setattr(floor, key, value)
                floor.save()
            else:
                # Create new floor
                Floor.objects.create(site=instance, **floor_data)

        # Remove floors that were not included in the update request
        for floor_number, floor in existing_floors.items():
            if floor_number not in processed_floors:
                floor.delete()

        return instance

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
