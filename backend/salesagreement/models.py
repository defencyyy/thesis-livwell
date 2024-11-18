from django.db import models
from django.utils import timezone
import uuid

class SalesAgreement (models.Model):
  customer_name = models.CharField(max_length=255)
  customer_email = models. EmailField()
  unit_title = models.CharField(max_length=255)
  site_name = models.CharField(max_length=255)
  unit_price = models. DecimalField(max_digits=10, decimal_places=2)
  payment_plan = models.CharField(max_length=255)
  spot_discount = models.DecimalField(max_digits=5, decimal_places=2)
  net_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
  other_charges = models.DecimalField(max_digits=10, decimal_places=2)
  total_amount_payable = models.DecimalField(max_digits=12, decimal_places=2)
  reservation_fee = models. DecimalField(max_digits=10, decimal_places=2)
  net_full_payment = models. DecimalField(max_digits=12, decimal_places=2)
  spot_downpayment = models. DecimalField(max_digits=10, decimal_places=2)
  spread_downpayment = models. DecimalField(max_digits=10, decimal_places=2)
  payable_months = models.IntegerField()
  payable_per_month = models. DecimalField(max_digits=10, decimal_places=2)
  balance_upon_turnover = models.DecimalField(max_digits=12, decimal_places=2)
  created_at = models.DateTimeField(default=timezone.now)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

  def _str_(self):
    return f"Sales Agreement for {self.customer_name}"
  
  def get_absolute_url(self):
    return f"/sales-agreement/{self.uuid}/"