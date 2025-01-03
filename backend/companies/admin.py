from django.contrib import admin
from .models import Company
from prbe.admin import custom_admin_site

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at') 
    list_display_links = ('id', 'name') 
    search_fields = ('name', 'description') 
    list_per_page = 25 

custom_admin_site.register(Company, CompanyAdmin)  