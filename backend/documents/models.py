from django.db import models
from companies.models import Company
from customers.models import Customer
from docreqs.models import Docreq 

class Document(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
  requirement = models.ForeignKey(Docreq, on_delete=models.CASCADE, null=True, blank=True) 
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=200)
  file = models.FileField(upload_to='documents/')
  is_verified = models.BooleanField(default=False)

  def __str__(self):
    return self.name
