from django.db import models
from companies.models import Company
from affiliations.models import Affiliation

class Site(models.Model):
  STATUS_CHOICES = [
    ('preselling', 'Preselling'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('sold_out', 'Sold Out'),
  ]

  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  picture = models.ImageField(upload_to='site_pictures/', blank=True, null=True)  
  affiliations = models.ManyToManyField(Affiliation, related_name='sites')
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  location = models.CharField(max_length=200)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='preselling')

  def __str__(self):
    return self.name
