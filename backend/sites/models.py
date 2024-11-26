from django.db import models
from companies.models import Company
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
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preselling')
    archived = models.BooleanField(default=False)

    # Location fields
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def location(self):
        """Constructs the full location string."""
        address_parts = [
            self.region,
            self.province,
            self.municipality,
            self.barangay if self.barangay else None, 
            f"Postal Code: {self.postal_code}" if self.postal_code else None, 
        ]
        # Filter out None or empty values and join with commas
        return ', '.join(filter(None, address_parts))
