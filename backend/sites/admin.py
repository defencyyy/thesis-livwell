from django.contrib import admin
from django.utils.html import mark_safe
from .models import Site, Floor
from prbe.admin import custom_admin_site
from django import forms

class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1  # Shows one empty form by default for adding new floors
    fields = ['floor_number']
    readonly_fields = ['floor_number']

    def get_queryset(self, request):
        """
        Fetch the floors for the current site being edited without using self.instance.
        """
        site_id = request.resolver_match.kwargs.get('object_id')  # Get the site ID from the URL
        queryset = super().get_queryset(request)
        if site_id:
            return queryset.filter(site_id=site_id)  # Filter floors based on the site_id
        return queryset

class SiteAdminForm(forms.ModelForm):
    add_multiple_floors = forms.IntegerField(min_value=1, required=False, label="Number of Floors to Add")

    class Meta:
        model = Site
        fields = '__all__'

    def save(self, commit=True):
        # Save the site instance first to generate a primary key
        site = super().save(commit=False)

        # Get the number of floors to add, defaulting to 0 if None
        num_floors = self.cleaned_data.get('add_multiple_floors', 0)
        
        # Ensure num_floors is an integer (if it's None, set it to 0)
        if num_floors is None:
            num_floors = 0

        # If we are adding multiple floors, create them
        if num_floors > 0:
            # Save the site first to ensure it has a primary key
            if commit:
                site.save()

            # After saving the site, create the floors
            max_floor_number = site.floors.count() + 1
            for i in range(num_floors):
                Floor.objects.create(site=site, floor_number=max_floor_number)
                max_floor_number += 1

        # Save the site instance if it hasn't been saved yet (in case commit was False)
        if commit:
            site.save()
        return site

class SiteAdmin(admin.ModelAdmin):
    form = SiteAdminForm  # Use the custom form for the SiteAdmin
    
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
