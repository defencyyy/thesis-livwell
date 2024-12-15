from django.db import models
from companies.models import Company
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.utils import timezone  
from django.core.validators import RegexValidator

class Broker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True, editable=True)
    contact_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                message="Enter a valid phone number (9 to 15 digits)."
            )
        ]
    )
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        self.username = self.username.lower()
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def total_sales(self):
        from sales.models import Sale  # Importing Sale here to avoid circular import
        return Sale.objects.filter(broker=self, status='Sold').count()

    @property
    def total_commissions(self):
        from sales.models import Sale  # Importing Sale here to avoid circular import
        return Sale.objects.filter(broker=self).aggregate(total_commission=models.Sum('commission'))['total_commission'] or 0

    def meets_sales_milestone(self, milestone):
        if milestone.type == "sales":
            return self.total_sales >= milestone.sales_threshold
        return False

    def meets_commission_milestone(self, milestone):
        if milestone.type == "commission":
            return self.total_commissions >= milestone.commission_threshold
        return False

    class Meta:
        ordering = ['last_name', 'first_name']
