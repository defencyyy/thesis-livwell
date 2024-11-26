from django.contrib import admin
from .models import Site
from prbe.admin import custom_admin_site

class SiteAdmin(admin.ModelAdmin):
    # Define the fields to display in the site list
    list_display = ('id', 'company', 'name', 'location', 'status', 'created_at', 'archived')
    
    # Define the fields that are clickable in the list display (links to the detail view)
    list_display_links = ('id', 'name')
    
    # Add search functionality for these fields
    search_fields = ('name', 'company__name', 'status', 'region', 'province', 'city')
    
    # Add filters for status and archived fields
    list_filter = ('status', 'archived', 'company')
    
    # Set how many entries are displayed per page
    list_per_page = 25
    
    # Add ordering by created_at (optional)
    ordering = ('-created_at',)

custom_admin_site.register(Site, SiteAdmin)
