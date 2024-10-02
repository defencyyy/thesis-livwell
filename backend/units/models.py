from django.db import models
from companies.models import Company
from affiliations.models import Affiliation

class Units(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  affiliations = models.ManyToManyField(Affiliation, related_name='units')
  # unit_name
  # unit_type

  # def __str__(self):
  #   return self.name
