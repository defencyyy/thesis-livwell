from django.db import models
from companies.models import Company
from affiliations.models import Affiliation

class Site(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  affiliations = models.ManyToManyField(Affiliation, related_name='sites')
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name