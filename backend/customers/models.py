from django.db import models
from brokers.models import Broker
from companies.models import Company
from units.models import Unit

class Customer(models.Model):
  broker = models.ForeignKey(Broker, on_delete=models.DO_NOTHING)
  email = models.EmailField(max_length=50) 
  contact_number = models.CharField(max_length=20)
  affiliated_link = models.URLField(blank=True)
  last_name = models.CharField(max_length=200, null=True)
  first_name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return f"{self.last_name}, {self.first_name}"
