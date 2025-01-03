from django.db import models
from companies.models import Company
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db.models import Max
from django.db import transaction

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
    relative_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    def save(self, *args, **kwargs):
        # Ensure company is set before saving the broker
        if self.company is None:
            raise ValueError("Company must be set before saving a broker.")

        # Ensure the username is always in lowercase
        self.username = self.username.lower()

        # Hash the password if it hasn't been hashed already
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        # Use a transaction to avoid race conditions
        with transaction.atomic():
            # First, save the instance without relative_id
            if self.relative_id is None:
                super().save(*args, **kwargs)  # Save without relative_id to get an ID

                # Now set the relative_id after the initial save
                self.relative_id = self.get_next_relative_id()
                self.save(update_fields=['relative_id'])
            else:
                # If relative_id is already set, save normally
                super().save(*args, **kwargs)

    def get_next_relative_id(self):
        # Fetch the max relative_id for brokers in the same company
        max_id = Broker.objects.filter(company=self.company).aggregate(Max('relative_id'))['relative_id__max']
        
        # If no brokers exist for the company, start from 1
        next_id = max_id + 1 if max_id else 1

        return next_id

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
        from sales.models import Sale  # Avoid circular import
        return Sale.objects.filter(broker=self, status='Sold').aggregate(
            total_commission=models.Sum('commission')
        )['total_commission'] or 0


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
        indexes = [
            models.Index(fields=['company', 'relative_id']),
        ]

