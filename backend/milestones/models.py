from django.db import models
from companies.models import Company

class Milestone(models.Model):
  STATUS_CHOICES = [
    ('broker', 'Broker'),
    ('company', 'Company'),
  ]
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)
  reward = models.CharField(max_length=100)
  type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='company')
  created_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name