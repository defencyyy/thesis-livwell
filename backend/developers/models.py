from django.db import models
from companies.models import Company
from django.contrib.auth.hashers import make_password

class Developer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, editable=False)
    contact_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)  

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    def get_username(self):
        return self.username  

    def get_email_field_name(self):
        return 'email' 