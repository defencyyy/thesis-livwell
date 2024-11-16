from django.contrib import admin
from .models import Developer
from prbe.admin import custom_admin_site

class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'first_name', 'last_name', 'email', 'contact_number')  
    list_display_links = ('id', 'first_name', 'last_name')  
    search_fields = ('first_name', 'last_name', 'company__name', 'email', 'username') 
    list_per_page = 25 

custom_admin_site.register(Developer, DeveloperAdmin)
