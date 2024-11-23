from django.db import models
from companies.models import Company
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
from django.utils import timezone  
from django.core.validators import RegexValidator

class Broker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True, editable=True)  # Set editable=False to prevent manual input
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

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Hash the password if not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
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

    class Meta:
        ordering = ['last_name', 'first_name']
