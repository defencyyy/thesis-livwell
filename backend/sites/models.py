from django.db import models
from companies.models import Company
from affiliations.models import Affiliation
import os

def logo_upload_path(instance, filename):
  company_id = instance.company.id if instance.company else 'new'
  return os.path.join('photos', str(company_id), 'sites', filename)

class Site(models.Model):
  STATUS_CHOICES = [
    ('preselling', 'Preselling'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('sold_out', 'Sold Out'),
  ]

  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  picture = models.ImageField(upload_to=logo_upload_path, blank=True, null=True)  
  affiliations = models.ManyToManyField(Affiliation, related_name='sites')
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preselling')

  def __str__(self):
    return self.name
