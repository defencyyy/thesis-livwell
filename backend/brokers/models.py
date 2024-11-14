from django.db import models
from companies.models import Company
from django.contrib.auth.hashers import make_password
from django.utils import timezone  

class Broker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20, blank=True, null=True)  # contact_number is optional now
    password = models.CharField(max_length=128)  # Default password will be handled in save method
    last_login = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        return f"{self.last_name}, {self.first_name} "
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def get_username(self):
        return self.username 

    def get_email_field_name(self):
        return 'email'
