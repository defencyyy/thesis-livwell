from django.contrib import admin
from django.utils.html import mark_safe
from .models import Site, Floor
from prbe.admin import custom_admin_site

# Inline to manage floors directly within the site admin page
class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1  # Shows one empty form by default for adding new floors
    fields = ['floor_number']
    readonly_fields = ['floor_number']

class SiteAdmin(admin.ModelAdmin):
    # Define the fields to display in the site list
    list_display = ('id', 'company', 'name', 'location', 'status', 'created_at', 'archived', 'image_preview')
    
    # Define the fields that are clickable in the list display (links to the detail view)
    list_display_links = ('id', 'name')
    
    # Add search functionality for these fields
    search_fields = ('name', 'company__name', 'status', 'region', 'province', 'municipality')
    
    # Add filters for status and archived fields
    list_filter = ('status', 'archived', 'company')
    
    # Set how many entries are displayed per page
    list_per_page = 25
    
    # Add ordering by created_at (optional)
    ordering = ('-created_at',)

    # Add FloorInline to allow floor management within the Site admin page
    inlines = [FloorInline]
    
    # Image preview for site logo
    def image_preview(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Logo Preview'

custom_admin_site.register(Site, SiteAdmin)

