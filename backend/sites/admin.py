from django.contrib import admin
from .models import Site
from prbe.admin import custom_admin_site

class SiteAdmin(admin.ModelAdmin):
  site_display = ('id', 'company', 'name', 'created_at', 'status')  
  site_display_links = ('id', 'name')  
  search_fields = ('name', 'company', 'description')
  site_per_page = 25 

custom_admin_site.register(Site, SiteAdmin)
