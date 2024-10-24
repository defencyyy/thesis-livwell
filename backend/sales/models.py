from django.db import models
from units.models import Unit
from customers.models import Customer
from brokers.models import Broker
from sites.models import Site

class Sale(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    date_sold = models.DateField(auto_now_add=True)

    # Make automatic

    def __str__(self):
      return f"Sale of {self.unit.title} to {self.customer.first_name} {self.customer.last_name}"
