from django.contrib import admin
from django.utils.html import mark_safe
from .models import Unit, UnitImage, UnitTemplate
from prbe.admin import custom_admin_site

class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1  # Shows one empty form by default for adding new images
    fields = ['image', 'uploaded_at', 'image_preview']
    readonly_fields = ['uploaded_at', 'image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_title', 'company', 'site', 'status', 'price', 'floor')
    list_display_links = ('id', 'unit_title')
    list_filter = ('status', 'company', 'site', 'view', 'balcony')
    search_fields = ('unit_title', 'company__name', 'site__name', 'description')
    list_per_page = 25
    
    # Add UnitImageInline to allow image management within the Unit admin page
    inlines = [UnitImageInline]

    def image_preview(self, obj):
        if obj.unitimage_set.exists():
            return mark_safe(f'<img src="{obj.unitimage_set.first().image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

custom_admin_site.register(Unit, UnitAdmin)

# UnitImage Admin
class UnitImageAdmin(admin.ModelAdmin):
    list_display = ('unit', 'image', 'uploaded_at', 'image_preview')
    search_fields = ('unit__unit_title',)
    list_filter = ('uploaded_at',)

    # Define the image preview method inside UnitImageAdmin
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

custom_admin_site.register(UnitImage, UnitImageAdmin)

