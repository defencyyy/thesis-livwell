from django.contrib import admin
from .models import Broker
from prbe.admin import custom_admin_site 

# Broker Admin
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'username', 'email', 'contact_number', 'first_name', 'last_name') 
    list_display_links = ('id', 'username') 
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company__name')  
    list_per_page = 25 


custom_admin_site.register(Broker, BrokerAdmin)  