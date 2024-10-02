from django.db import models
from companies.models import Company

class Affiliation(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  is_active = models.BooleanField(default=True)
  
  def __str__(self):
    return self.name
