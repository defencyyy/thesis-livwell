from django.contrib import admin
from .models import Unit

class UnitAdmin(admin.ModelAdmin):
  unit_display = ('id', 'unit_title', 'company', 'site', 'status', 'price', 'quantity', 'floor')
  unit_display_links = ('id', 'unit_title')
  unit_filter = ('status', 'company', 'site', 'view', 'balcony')
  search_fields = ('unit_title', 'company_name', 'site_name', 'description')
  unit_per_page = 25

# Register the Unit model with the customized admin interface
admin.site.register(Unit, UnitAdmin)