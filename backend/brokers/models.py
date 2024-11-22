from django.db import models
from companies.models import Company
from django.contrib.auth.hashers import make_password
from django.utils import timezone  
from django.core.validators import RegexValidator

class Broker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True, editable=True)  # Set editable=False to prevent manual input
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
        return f"{self.last_name}, {self.first_name} "
    
    def save(self, *args, **kwargs):
        # Hash the password if not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def get_username(self):
        return self.username 

    def get_email_field_name(self):
        return 'email'
