from django.db import models
from companies.models import Company
from sites.models import Site
import os, re

def logo_upload_path(instance, filename):
    company_name = instance.unit.company.name if instance.unit and instance.unit.company else 'new_company'
    site_name = instance.unit.site.name if instance.unit and instance.unit.site else 'new_site'
    unit_id = instance.unit.id if instance.unit else 'new_unit'
    
    company_name = re.sub(r'\s+', '_', company_name) 
    company_name = re.sub(r'[^\w\s-]', '', company_name)  
    
    site_name = re.sub(r'\s+', '_', site_name) 
    site_name = re.sub(r'[^\w\s-]', '', site_name) 
    
    filename = filename or 'unit_image.jpg' 
    
    # The new file path will include the unit_id
    return os.path.join('photos', company_name, 'sites', site_name, 'units', str(unit_id), filename)


class Unit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    ]
    VIEW_CHOICES = [
        ('south', 'South'),
        ('north', 'North'),
        ('east', 'East'),
        ('west', 'West'),
    ]
    BALCONY_CHOICES = [
        ('has_balcony', 'Has Balcony'),
        ('no_balcony', 'No Balcony'),
    ]

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    unit_title = models.CharField(max_length=100)
    bedroom = models.PositiveIntegerField(default=1, null=True)
    bathroom = models.PositiveIntegerField(default=1, null=True)
    floor_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lot_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    floor = models.PositiveIntegerField(default=1, help_text="Floor number")
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    view = models.CharField(max_length=10, choices=VIEW_CHOICES, blank=True)
    balcony = models.CharField(max_length=20, choices=BALCONY_CHOICES, blank=True)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, 
        help_text="Commission earned when the unit is sold"
    )

    def __str__(self):
        return f"{self.site.name} - {self.unit_title}"


class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=logo_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.unit.unit_title}"

    # unit_number = models.PositiveIntegerField(null=True) # Eto ung gawin natin na parang Floor 10 Unit 1 = 10001 or 1001, floor+unitqty check mo ung sa baba

    # final_id 21 (20) = 2 21002 21003 ... 21020
    # final_id 21 (20) = 21021 ... 21040
    # sites
    # 25 floors
    # floor 21 = 100 space
    # select 1-20 / select 1,5,7,10
    # 2101 2102 ... 2119 2120 / 2101, 2105, 2107, 2110
    # def unit_type
