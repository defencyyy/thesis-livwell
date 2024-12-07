from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from companies.models import Company
from sites.models import Site, Floor
import os, re

def logo_upload_path(instance, filename):
    company_name = instance.unit.company.name if instance.unit and instance.unit.company else 'new_company'
    site_name = instance.unit.site.name if instance.unit and instance.unit.site else 'new_site'

    company_name = re.sub(r'\s+', '_', company_name)
    company_name = re.sub(r'[^\w\s-]', '', company_name)  
    site_name = re.sub(r'\s+', '_', site_name)
    site_name = re.sub(r'[^\w\s-]', '', site_name)

    if instance.image_type == 'unit':
        unit_id = instance.unit.id if instance.unit else 'new_unit'
        image_count = instance.unit.images.count() if instance.unit else 0
        filename = f'unit_image_{image_count + 1}.jpg'
        
        return os.path.join('photos', company_name, 'sites', site_name, 'units', str(unit_id), filename)

    elif instance.image_type == 'unit_template':
        template_id = instance.unit_template.id if instance.unit_template else 'new_template'
        template_name = instance.unit_template.name if instance.unit_template else 'new_template'
        image_count = instance.unit_template.images.count() if instance.unit_template else 0
        filename = f'template_image_{image_count + 1}.jpg'

        template_name = re.sub(r'\s+', '_', template_name)
        template_name = re.sub(r'[^\w\s-]', '', template_name)

        filename = f'template_image_{image_count}.jpg'
        
        return os.path.join('photos', company_name, 'sites', site_name, 'unit_templates', f'{template_id}_{template_name}', filename)
    
    return os.path.join('photos', company_name, 'unknown', filename)

def get_default_unit_type():
    # Define all default unit types
    default_unit_types = [
        'Studio', 
        'Studio Deluxe', 
        '1 Bedroom', 
        '2 Bedroom', 
        '3 Bedroom', 
        'Penthouse', 
        'Loft', 
    ]
    
    UnitType = apps.get_model('units', 'UnitType')
    
    # Create all default unit types if they don't exist
    for unit_type in default_unit_types:
        UnitType.objects.get_or_create(
            name=unit_type, 
            defaults={'is_custom': False}
        )
    
    # Return the "Studio" type by default for units
    default_unit_type, created = UnitType.objects.get_or_create(
        name='Studio', defaults={'is_custom': False}
    )
    return default_unit_type.id
    
class UnitType(models.Model):
    DEFAULT_CHOICES = [
        'Studio', 
        'Studio Deluxe', 
        '1 Bedroom', 
        '2 Bedroom', 
        '3 Bedroom', 
        'Penthouse', 
        'Loft', 
    ]

    name = models.CharField(max_length=50, unique=True)
    is_custom = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        # Prevent modification of default unit types
        if not self.is_custom and self.pk:
            raise ValueError("Default unit types cannot be modified.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Unit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending reservation', 'Pending Reservation'),
        ('reserved', 'Reserved'),
    ]
    VIEW_CHOICES = [
        ('south', 'South'),
        ('north', 'North'),
        ('east', 'East'),
        ('west', 'West'),
    ]
    BALCONY_CHOICES = [
        ('has balcony', 'Has Balcony'),
        ('no balcony', 'No Balcony'),
    ]
    unit_type = models.ForeignKey(
        'UnitType', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="units", 
        default=get_default_unit_type,
        help_text="Type of the Unit (e.g., Studio, 1 Bedroom, etc.)",
    )
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    unit_template = models.ForeignKey('UnitTemplate', related_name='units', null=True, blank=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name="units")
    unit_number = models.CharField(
        max_length=10,
        blank=True,
        help_text="Auto-generated Unit Number (e.g., 21001)"
    )
    unit_title = models.CharField(max_length=100, blank=True)
    bedroom = models.PositiveIntegerField(default=1, null=True)
    bathroom = models.PositiveIntegerField(default=1, null=True)
    floor_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lot_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    view = models.CharField(max_length=10, choices=VIEW_CHOICES, blank=True, null=True)
    balcony = models.CharField(max_length=20, choices=BALCONY_CHOICES, blank=True, null=True)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, null=True,
        help_text="Commission earned when the unit is sold"
    )
    spot_discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        help_text="Spot discount percentage"
    )
    spot_discount_flat = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="Flat spot discount amount"
    )
    reservation_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    other_charges = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)

    def save(self, *args, **kwargs):
        if self.status:
            self.status = self.status.capitalize()

        # Validate that the floor belongs to the same site
        if self.floor.site != self.site:
            raise ValueError("The selected floor does not belong to the specified site.")
        
        # Validate positive areas
        if self.floor_area is not None and self.floor_area <= 0:
            raise ValueError("Floor area must be a positive value.")
        if self.lot_area is not None and self.lot_area <= 0:
            raise ValueError("Lot area must be a positive value.")

        # Pull default values from the Site if not set
        if not self.commission:
            self.commission = self.site.commission
        if not self.spot_discount_percentage:
            self.spot_discount_percentage = self.site.spot_discount_percentage
        if not self.spot_discount_flat:
            self.spot_discount_flat = self.site.spot_discount_flat
        if not self.reservation_fee:
            self.reservation_fee = self.site.reservation_fee
        if not self.other_charges:
            self.other_charges = self.site.other_charges
        if not self.vat_percentage:
            self.vat_percentage = self.site.vat_percentage

        # Auto-generate unit number if not set
        if not self.unit_number:
            unit_count = Unit.objects.filter(floor=self.floor).count() + 1
            self.unit_number = f"{self.floor.floor_number:02d}{unit_count:03d}"

        # Auto-generate unit title if not set
        if not self.unit_title:
            self.unit_title = f"{self.unit_type.name} - {self.unit_number}"

        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['site', 'status']),
        ]

    def __str__(self):
        return f"{self.site.name} - {self.unit_title}"

class UnitTemplate(models.Model):
    unit_type = models.ForeignKey(
        'UnitType', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="unit_templates", 
        default=get_default_unit_type,
        help_text="Type of the Unit (e.g., Studio, 1 Bedroom, etc.)",
    )
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, unique=True)
    bedroom = models.PositiveIntegerField(default=1)
    bathroom = models.PositiveIntegerField(default=1)
    floor_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lot_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    view = models.CharField(max_length=10, choices=Unit.VIEW_CHOICES)
    balcony = models.CharField(max_length=20, choices=Unit.BALCONY_CHOICES)
    commission = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    description = models.TextField(blank=True, help_text="Description of the template")
    last_updated = models.DateTimeField(auto_now=True)
    primary_image = models.ForeignKey('UnitImage', null=True, blank=True, on_delete=models.SET_NULL, related_name='primary_for_templates', help_text="Primary image for the template")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "bedroom": self.bedroom,
            "bathroom": self.bathroom,
            "floor_area": self.floor_area,
            "lot_area": self.lot_area,
            "price": self.price,
            "view": self.view,
            "balcony": self.balcony,
            "commission": self.commission,
        }

def validate_image_size(image):
    filesize = image.file.size
    limit = 5 * 1024 * 1024  # Limit image size to 5 MB
    if filesize > limit:
        raise ValidationError("Maximum size of the image is 5 MB")

class UnitImage(models.Model):
    IMAGE_TYPE_CHOICES = [
        ('unit', 'Unit'),
        ('unit_template', 'Unit Template'),
    ]

    unit = models.ForeignKey(Unit, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    unit_template = models.ForeignKey(UnitTemplate, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES)
    image = models.ImageField(upload_to=logo_upload_path, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), 
        validate_image_size,  
    ])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    primary = models.BooleanField(default=False, help_text="Indicates if this image is the primary image for the template")

    def __str__(self):
        if self.image_type == 'unit':
            return f"Image for {self.unit.unit_title}"
        else:
            return f"Image for {self.unit_template.name}"

    def save(self, *args, **kwargs):
        # Ensure that either unit or unit_template is set, not both
        if self.image_type == 'unit' and not self.unit:
            raise ValueError("Unit must be set when the image type is 'unit'")
        if self.image_type == 'unit_template' and not self.unit_template:
            raise ValueError("Unit Template must be set when the image type is 'unit_template'")

        # Ensure only one primary image per template
        if self.image_type == 'unit_template' and self.primary:
            UnitImage.objects.filter(unit_template=self.unit_template, primary=True).update(primary=False)

        super().save(*args, **kwargs)