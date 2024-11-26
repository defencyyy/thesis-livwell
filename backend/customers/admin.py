from django.contrib import admin
from .models import Customer
from prbe.admin import custom_admin_site

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name', 'email', 'contact_number')  
    list_display_links = ('id', 'name') 
    search_fields = ('name', 'company__name', 'email', 'username', 'description')  
    list_per_page = 25  

custom_admin_site.register(Customer, CustomerAdmin)  