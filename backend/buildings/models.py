from django.db import models
from companies.models import Company

class Building(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200)
  is_active = models.BooleanField(default=True)
  
  def __str__(self):
    return self.name
