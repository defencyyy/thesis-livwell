from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from .models import Broker

class BrokerAdmin(admin.ModelAdmin):
    broker_display = ('id', 'company', 'username', 'email', 'contact_number', 'first_name', 'last_name') 
    broker_display_links = ('id', 'username') 
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company__name') 
    broker_per_page = 25

admin.site.register(Broker, BrokerAdmin)
