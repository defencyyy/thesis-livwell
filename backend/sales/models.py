from django.db import models
from units.models import Unit
from customers.models import Customer
from brokers.models import Broker
from sites.models import Site
from companies.models import Company
import os

def reservation_file_upload_path(instance, filename):
    company_name = instance.company.name if instance.company else 'new_company'
    sale_id = instance.id if instance.id else 'new_sale'

    filename = 'reservation.pdf' if filename is None else filename
    return os.path.join('files', str(company_name), 'sales', str(sale_id), filename)

class Sale(models.Model):
    STATUS_CHOICES = [
        ('Pending Reservation', 'Pending Reservation'),  # Reservation submitted, awaiting confirmation
        ('Reserved', 'Reserved'),  # Reservation confirmed, unit is on hold
        ('Pending Sold', 'Pending Sold'),  # Reservation complete, awaiting final sale confirmation
        ('Sold', 'Sold')  # Sale confirmed, unit officially sold
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other')
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_sold = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_reservation')

    # New fields
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid as reservation fee
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)  # Cash, card, transfer
    payment_reference = models.CharField(max_length=100, blank=True, null=True)  # Optional reference (e.g., transaction ID)
    reservation_file = models.FileField(upload_to=reservation_file_upload_path, blank=True, null=True)  # Optional file upload

    def __str__(self):
        return f"Sale of {self.unit.unit_title} to {self.customer.first_name} {self.customer.last_name}"
