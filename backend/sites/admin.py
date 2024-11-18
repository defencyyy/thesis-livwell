from django.contrib import admin
from .models import Site

class SiteAdmin(admin.ModelAdmin):
  site_display = ('id', 'company', 'name', 'created_at', 'status')  
  site_display_links = ('id', 'name')  
  search_fields = ('name', 'company', 'description')
  site_per_page = 25 

admin.site.register(Site, SiteAdmin)
