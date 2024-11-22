from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
  company_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')  
  company_display_links = ('id', 'name')  
  search_fields = ('name', 'description')
  company_per_page = 25 

admin.site.register(Company, CompanyAdmin)
