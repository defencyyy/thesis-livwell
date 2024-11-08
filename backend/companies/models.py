from django.db import models

class Company(models.Model):
  name = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  logo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  is_active = models.BooleanField(default=True)
  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = ("Company") 
    verbose_name_plural = ("Companies")