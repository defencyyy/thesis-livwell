from django.db import models

class Milestone(models.Model):
  STATUS_CHOICES = [
    ('broker', 'Broker'),
    ('company', 'Company'),
  ]

  name = models.CharField(max_length=100, unique=True)
  description = models.TextField(blank=True)
  reward = models.CharField(max_length=100)
  type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='company')
  created_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name