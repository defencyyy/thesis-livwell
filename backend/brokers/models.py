from django.db import models
from companies.models import Company
from affiliations.models import Affiliation
from django.contrib.auth.hashers import make_password
from django.utils import timezone  

class Broker(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    affiliations = models.ManyToManyField(Affiliation, related_name='brokers')
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128, null=True)
    last_login = models.DateTimeField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} "
    
    def get_username(self):
        return self.username 

    def get_email_field_name(self):
        return 'email' 
