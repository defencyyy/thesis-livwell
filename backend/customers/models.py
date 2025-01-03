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
    archived = models.BooleanField(default=False)
    customer_code = models.CharField(max_length=10)  # Removed unique=True

    class Meta:
        unique_together = ('broker', 'customer_code')  # Added unique constraint

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def save(self, *args, **kwargs):
        if not self.customer_code:
            last_code = (
                Customer.objects.filter(broker=self.broker)
                .order_by('-customer_code')
                .first()
            )

            if last_code:
                last_num = int(last_code.customer_code.split('-')[1])
                new_code = f"CUST-{str(last_num + 1).zfill(3)}"
            else:
                new_code = "CUST-001"

            self.customer_code = new_code

        super().save(*args, **kwargs)
