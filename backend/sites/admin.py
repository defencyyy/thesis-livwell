from django.contrib import admin
from django.utils.html import mark_safe
from .models import Site, Section
from prbe.admin import custom_admin_site
from django import forms

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1  # Shows one empty form by default for adding new sections
    fields = ['number', 'name']
    readonly_fields = ['number', 'name']

    def get_queryset(self, request):
        site_id = request.resolver_match.kwargs.get('object_id')  # Get the site ID from the URL
        queryset = super().get_queryset(request)
        if site_id:
            return queryset.filter(site_id=site_id)  # Filter sections based on the site_id
        return queryset

class SiteAdminForm(forms.ModelForm):
    add_multiple_sections = forms.IntegerField(min_value=1, required=False, label="Number of sections to Add")

    class Meta:
        model = Site
        fields = '__all__'

    def save(self, commit=True):
        site = super().save(commit=False)

        # Get the number of sections to add, defaulting to 0 if None
        num_sections = self.cleaned_data.get('add_multiple_sections', 0)

        if num_sections > 0:
            # Save the site first to ensure it has a primary key
            if commit:
                site.save()

                # After saving the site, create the sections
                max_section_number = site.sections.count() + 1
                for i in range(num_sections):
                    # Generate the section name based on the numbering type
                    section_name = Section(
                        site=site,
                        number=max_section_number,
                        name=self.generate_next_section_name(site)  # Generate section name dynamically
                    )
                    section_name.save()
                    max_section_number += 1

        if commit:
            site.save()
        return site

    def generate_next_section_name(self, site):
        # Get the last section created for this site
        last_section = site.sections.order_by('-number').first()

        # Call the appropriate naming method based on numbering type (numeric or alphabetic)
        if site.numbering_type == 'numeric':
            return self.generate_numeric_section_name(last_section)
        elif site.numbering_type == 'alphabetic':
            return self.generate_alphabetic_section_name(last_section)

    def generate_numeric_section_name(self, last_section):
        # Numeric sequence: 1, 2, 3...
        if not last_section:
            return "1"
        next_number = last_section.number + 1
        return str(next_number)

    def generate_alphabetic_section_name(self, last_section):
        # Alphabetic sequence: A, B, C...Z, AA, AB, etc.
        if not last_section:
            return "A"  # First section
        
        last_name = last_section.name
        # Check if last section name is numeric or alphabetic
        if last_name[-1].isalpha():
            next_char = chr(ord(last_name[-1]) + 1)  # Increment letter (A -> B)
            if next_char > 'Z':
                next_char = 'A'
                next_number = last_section.number + 1
                return f"{next_number}{next_char}"
            return next_char
        else:
            # Handle numeric naming, should not happen in alphabetic naming but let's be safe
            return str(last_section.number + 1)
        
class SiteAdmin(admin.ModelAdmin):
    form = SiteAdminForm  # Use the custom form for the SiteAdmin

    list_display = ('id', 'company', 'name', 'location', 'status', 'created_at', 'archived', 'image_preview')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'company__name', 'status', 'region', 'province', 'municipality')
    list_filter = ('status', 'archived', 'company')
    list_per_page = 25
    ordering = ('-created_at',)
    inlines = [SectionInline]  # Inline to manage sections from the Site admin page

    def image_preview(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Logo Preview'

custom_admin_site.register(Site, SiteAdmin)
