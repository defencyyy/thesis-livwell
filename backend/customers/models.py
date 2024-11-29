from django.db import models
from brokers.models import Broker
from companies.models import Company
from django.db.models import Max

class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE) 
    broker = models.ForeignKey(Broker, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=50)
    contact_number = models.CharField(max_length=20)
    last_name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    
    # Default value will be overridden in save method
    customer_code = models.CharField(max_length=10, unique=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    # Overriding the save method to automatically generate a unique customer code in the format CUST-001
    def save(self, *args, **kwargs):
        if not self.customer_code:
            # Get the latest customer code number (if any)
            last_code = Customer.objects.aggregate(Max('customer_code'))['customer_code__max']

            if last_code:
                # Extract the number part of the last code and increment it
                last_num = int(last_code.split('-')[1])
                new_code = f"CUST-{str(last_num + 1).zfill(3)}"  # Increment and zero-pad
            else:
                # If no customers exist, start from 001
                new_code = "CUST-001"
            
            self.customer_code = new_code  # Set the new unique customer code

        super().save(*args, **kwargs)
