from django.db import models
from units.models import Unit
from customers.models import Customer
from brokers.models import Broker
from sites.models import Site
from companies.models import Company

class Sale(models.Model):
  STATUS_CHOICES = [
        ('pending', 'Pending'),  # Waiting for documents or downpayment
        ('under review', 'Under Review'),  # Awaiting developer's approval
        ('sold', 'Sold')  # Sale confirmed by developer
    ]
  site = models.ForeignKey(Site, on_delete=models.CASCADE)
  unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE) 
  date_sold = models.DateField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


  def __str__(self):
    return f"Sale of {self.unit.unit_title} to {self.customer.first_name} {self.customer.last_name}"