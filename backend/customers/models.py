from django.db import models
from brokers.models import Broker
from companies.models import Company

class Customer(models.Model):
  company = models.ForeignKey(Company, on_delete=models.CASCADE) 
  broker = models.ForeignKey(Broker, on_delete=models.DO_NOTHING)
  email = models.EmailField(max_length=50)
  contact_number = models.CharField(max_length=20)
  affiliated_link = models.URLField(blank=True)
  last_name = models.CharField(max_length=200, null=True)
  first_name = models.CharField(max_length=200, null=True)

  @property
  def name(self):
      return f"{self.first_name} {self.last_name}"

  def __str__(self):
    return f"{self.last_name}, {self.first_name}"