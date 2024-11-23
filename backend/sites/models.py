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

  filename = filename or 'site_logo.jpg' 

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
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preselling')
  # amenities

  def __str__(self):
    return self.name
