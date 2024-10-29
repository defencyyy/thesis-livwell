from django.db import models
import os

def logo_upload_path(instance, filename):
  company_id = instance.id if instance.id else 'new'
  return os.path.join('photos', str(company_id), 'logo', filename)

class Company(models.Model):
  name = models.CharField(max_length=100, unique=True, editable=True)
  description = models.TextField(blank=True)
  is_active = models.BooleanField(default=True)
  logo = models.ImageField(upload_to=logo_upload_path, blank=True) 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Company"
    verbose_name_plural = "Companies"

