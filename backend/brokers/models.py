from django.db import models
from companies.models import Company
from affiliations.models import Affiliation
from django.contrib.auth.hashers import make_password

class Broker(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  affiliations = models.ManyToManyField(Affiliation, related_name='brokers')
  email = models.CharField(max_length=50)
  username = models.CharField(max_length=100)
  name = models.CharField(max_length=200)
  contact_number = models.CharField(max_length=20)
  description = models.TextField(blank=True)
  picture = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  password = models.CharField(max_length=128, blank=True, null=True)


  def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
  

  def __str__(self):
    return self.name
