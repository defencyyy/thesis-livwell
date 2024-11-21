from django.db import models
from django.utils import timezone
from django.urls import reverse
from units.models import Unit
from customers.models import Customer
from brokers.models import Broker
from sites.models import Site
import uuid

class SalesDetails(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)

    
    # Payment Plan
    payment_plan = models.CharField(max_length=255)  # Can be 'spot_cash' or 'in_house_financing'

    # Spot Discount (percentage)
    spot_discount_percent = models.DecimalField(max_digits=5, decimal_places=2)  # Spot discount percentage (e.g., 5.00 for 5%)
    
    # TLP Discount (percentage)
    tlp_discount_percent = models.DecimalField(max_digits=5, decimal_places=2)  # TLP discount percentage (e.g., 5.00 for 5%)

    # Other charges (percentage)
    other_charges_percent = models.DecimalField(max_digits=5, decimal_places=2)  # Other charges percentage (e.g., 8.50 for 8.5%)
    

    # Spot Downpayment (percentage)
    spot_downpayment_percent = models.DecimalField(max_digits=5, decimal_places=2)  # Spot downpayment percentage (e.g., 10.00 for 10%)
    
    # Reservation fee
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Reservation fee (flat value, e.g., 30000)

    # Spread Downpayment (percentage)
    spread_downpayment_percent = models.DecimalField(max_digits=5, decimal_places=2)  # Spread downpayment percentage (e.g., 15.00 for 15%)
    
    # Payment Terms
    payable_months = models.IntegerField()  # Number of months to pay
    payable_per_month = models.DecimalField(max_digits=10, decimal_places=2)  # Amount to be paid monthly

    # Final balance upon turnover
    balance_upon_turnover = models.DecimalField(max_digits=12, decimal_places=2)  # Balance left to be paid upon turnover

    # Other financial details
    net_unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Net price after discount (spot + TLP)
    total_amount_payable = models.DecimalField(max_digits=12, decimal_places=2)  # Total amount payable (net unit price + other charges)
    net_full_payment = models.DecimalField(max_digits=12, decimal_places=2)  # Net full payment (after reservation fee)

    # Date of creation of the sales agreement
    created_at = models.DateTimeField(default=timezone.now)
    
    # Unique identifier for the agreement
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Sales Agreement for {self.customer}"

    def get_absolute_url(self):
        return reverse('sales-agreement-detail', kwargs={'uuid': self.uuid})
