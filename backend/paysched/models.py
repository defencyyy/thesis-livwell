from django.db import models
from companies.models import Company
from units.models import Unit

class PaymentSchedule(models.Model):
  company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='payment_schedules')
  title = models.CharField(max_length=100)
  # Insert calculation

  def __str__(self):
    return self.title