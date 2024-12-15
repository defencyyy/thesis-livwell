from rest_framework import serializers
from .models import Site, Company, Section

class SectionSerializer(serializers.ModelSerializer):
    total_units = serializers.SerializerMethodField()
    available_units = serializers.SerializerMethodField()
    
    class Meta:
        model = Section
        fields = ['id', 'number', 'name', 'total_units', 'available_units']

    def get_total_units(self, obj):
        return obj.units.count()

    def get_available_units(self, obj):
        return obj.units.filter(status='Available').count()

class SiteSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    sections = serializers.SerializerMethodField()
    number_of_sections = serializers.IntegerField(write_only=True, required=False)
    numbering_type = serializers.CharField( required=False)
    section_label = serializers.CharField( required=False)
    picture = serializers.ImageField(required=False, allow_null=True)

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
            'address',
            'status',
            'created_at',
            'archived',
            'sections',
            'number_of_sections',
            'numbering_type', 
            'section_label',  
            'maximum_months',
            'commission',
            'spot_discount_percentage',
            'spot_discount_flat',
            'vat_percentage',
            'reservation_fee',
            'other_charges',
            'relative_id',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        number_of_sections = validated_data.pop('number_of_sections', 0)
        numbering_type = validated_data.pop('numbering_type', 'numeric')
        section_label = validated_data.pop('section_label', 'floor')

        # Create the site instance first
        site = super().create(validated_data)

        # Optionally, you can assign numbering_type and section_label to your site model if necessary
        site.numbering_type = numbering_type
        site.section_label = section_label
        site.save()

        # Create sections based on the number_of_sections and numbering_type
        for i in range(1, number_of_sections + 1):
            # Generate the section name based on the numbering type (numeric or alphabetic)
            section_name = self.generate_section_name(site, i)

            # Create the section with dynamic name
            Section.objects.create(site=site, number=i, name=section_name)

        return site

    def update(self, instance, validated_data):
        # Extract sections data from validated_data
        sections_data = validated_data.pop('sections', [])

        # Update fields of the site instance
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # If the 'picture' field is included in the validated_data, update the instance picture
        picture_file = validated_data.get('picture', None)
        if picture_file:
            instance.picture = picture_file

        instance.save()

        # Retrieve existing sections for the site
        existing_sections = {section.number: section for section in instance.sections.all()}

        # Keep track of processed sections
        processed_sections = set()

        # Iterate through incoming sections data
        for section_data in sections_data:
            section_number = section_data['number']
            processed_sections.add(section_number)

            if section_number in existing_sections:
                # Update existing section (if it already exists)
                section = existing_sections[section_number]
                for key, value in section_data.items():
                    setattr(section, key, value)
                section.save()
            else:
                # Create new section (if it doesn't exist)
                Section.objects.create(site=instance, **section_data)

        # Append sections based on number_of_sections and numbering_type if no sections are provided
        number_of_sections = validated_data.get('number_of_sections', 0)
        if number_of_sections:
            last_section_number = max(existing_sections.keys(), default=0)
            for i in range(last_section_number + 1, last_section_number + number_of_sections + 1):
                section_name = self.generate_section_name(instance, i)
                Section.objects.create(site=instance, number=i, name=section_name)

        return instance

    def generate_section_name(self, site, section_number):
        """Generate the section name based on the numbering type and section label."""
        last_section = site.sections.order_by('-number').first()

        if site.numbering_type == 'numeric':
            return str(section_number)

        elif site.numbering_type == 'alphabetic':
            if not last_section:
                return "A"  # Start with "A" if no previous section
            else:
                return self.generate_alphabetic_name(last_section)

    def generate_alphabetic_name(self, last_section):
        """Generate an alphabetic name sequence (A, B, C, ..., Z, AA, AB, ...)."""
        last_name = last_section.name
        if last_name[-1].isalpha():
            next_char = chr(ord(last_name[-1]) + 1)
            if next_char > 'Z':
                next_char = 'A'
                next_number = last_section.number + 1
                return f"{next_number}{next_char}"
            return next_char
        else:
            return str(last_section.number + 1)

    def validate_status(self, value):
        """Ensure the status is within the allowed choices."""
        valid_statuses = [choice[0] for choice in Site.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status '{value}'. Allowed statuses are: {', '.join(valid_statuses)}.")
        return value

    def validate_picture(self, value):
        """Optional: Ensure the picture file is not too large and is a valid image type."""
        if value:
            max_size = 10 * 1024 * 1024  # 5 MB max size
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            
            if value.size > max_size:
                raise serializers.ValidationError("The picture file is too large. Maximum size is 5MB.")
            
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(f"Invalid image type. Allowed types are: {', '.join(allowed_types)}.")
        return value

    def validate_maximum_months(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Maximum months must be an integer.")
        if value < 0:
            raise serializers.ValidationError("Maximum months cannot be negative.")
        return value

    def validate(self, data):
        """Additional validation for required fields (if they are not included in 'required' attribute)."""
        required_fields = ['name', 'region', 'province', 'municipality', 'barangay', 'status']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f"{field} is required and cannot be empty.")
        return data

    def get_sections(self, obj):
        sections_with_counts = obj.section_with_unit_counts()
        return sections_with_counts
