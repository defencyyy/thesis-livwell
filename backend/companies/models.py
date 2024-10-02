from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  logo = models.ImageField(upload_to='photos/%Y/%m/%d/')
  
  def __str__(self):
    return self.name
