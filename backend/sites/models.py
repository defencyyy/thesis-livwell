from django.db import models
from companies.models import Company
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
import os, re

def logo_upload_path(instance, filename):
  company_name = instance.company.name if instance.company else 'new_company'
  company_name = re.sub(r'\s+', '_', company_name) 
  company_name = re.sub(r'[^\w\s-]', '', company_name)

  site_name = instance.name if instance.name else 'new_site'
  site_name = re.sub(r'\s+', '_', site_name) 
  site_name = re.sub(r'[^\w\s-]', '', site_name)  

  # Prevent overwriting by including the original filename
  file_extension = filename.split('.')[-1]
  filename = f'{site_name}_logo.{file_extension}'
  
  return os.path.join('photos', company_name, 'sites', site_name, filename)

class Site(models.Model):
    STATUS_CHOICES = [
        ('preselling', 'Preselling'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('sold_out', 'Sold Out'),
    ]

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    picture = models.ImageField(upload_to=logo_upload_path, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="No description provided")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preselling')
    archived = models.BooleanField(default=False)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Pricing Defaults
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, null=True,
        help_text="Commission earned when the unit is sold"
    )
    spot_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    spot_discount_flat = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    reservation_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    other_charges = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Maximum months (e.g., for loan term)
    maximum_months = models.PositiveIntegerField(default=60, help_text="Maximum months for payment term (e.g., 60 months for 5 years max)")

    def __str__(self):
        return self.name

    @property
    def location(self):
        address_parts = [
            self.region,
            self.province,
            self.municipality,
            self.barangay, 
            f"Postal Code: {self.postal_code}" if self.postal_code else None, 
        ]
        return ', '.join(filter(None, address_parts))

    @property
    def total_units(self):
        # Using annotate to count the units per section
        from units.models import Unit
        return Unit.objects.filter(site=self).count()

    @property
    def available_units(self):
        # Using annotate to count available units per section
        from units.models import Unit
        return Unit.objects.filter(site=self, status='Available').count()

    def section_with_unit_counts(self):
        # This method returns sections with unit counts and available unit counts.
        return (
            self.sections
            .annotate(
                total_units=Count('units'),
                available_units=Count('units', filter=Q(units__status='Available'))
            )
            .values('id', 'number', 'total_units', 'available_units')
        )

    def create_units(self, units_per_section, template=None):
        from units.models import Unit
        if units_per_section <= 0:
            raise ValueError("Units per section must be a positive integer.")
        
        if not template:
            template = {
                "bedroom": 1,
                "bathroom": 1,
                "floor_area": 50.0,
                "lot_area": 0.0,
                "price": 1000000.0,
                "status": "available",
                "view": "south",
                "balcony": "no balcony",
                "commission": 0.0,
            }
        
        created_units = []
        for section in self.sections.all(): 
            for unit_number in range(1, units_per_section + 1):
                unit = Unit(
                    company=self.company,
                    site=self,
                    section=section.number,
                    unit_number=f"{section.name}{unit_number:03d}",
                    unit_title=f"Unit {section.name}-{unit_number}",
                    bedroom=template.get("bedroom"),
                    bathroom=template.get("bathroom"),
                    floor_area=template.get("floor_area"),
                    lot_area=template.get("lot_area"),
                    price=template.get("price"),
                    status=template.get("status"),
                    view=template.get("view"),
                    balcony=template.get("balcony"),
                    commission=template.get("commission"),
                )
                created_units.append(unit)
        
        Unit.objects.bulk_create(created_units)
        return len(created_units)

class Section(models.Model):
    # This model represents sections such as floors (condos), blocks (subdivisions), or levels (parking).
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50) 
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"Section {self.name} - {self.site.name}"
        
