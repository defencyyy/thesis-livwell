from django.contrib import admin
from django.utils.html import mark_safe
from .models import Unit, UnitImage, UnitTemplate, UnitType
from prbe.admin import custom_admin_site

# Inline admin for `UnitImage` in both Unit and UnitTemplate
class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1
    fields = ('image', 'image_type', 'uploaded_at', 'image_preview')
    readonly_fields = ('uploaded_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Preview'

# Unit admin with inline images
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'unit_title', 'company', 'site', 'floor', 'status', 'price', 'view', 'balcony')
    search_fields = ('unit_title', 'company__name', 'site__name')
    list_filter = ('company', 'status', 'view', 'balcony')
    inlines = [UnitImageInline]

custom_admin_site.register(Unit, UnitAdmin)

# UnitTemplate admin with inline images
class UnitTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'bedroom', 'bathroom', 'floor_area', 'price', 'view', 'balcony')
    search_fields = ('name', 'description')
    list_filter = ('company', 'view', 'balcony')
    inlines = [UnitImageInline]

custom_admin_site.register(UnitTemplate, UnitTemplateAdmin)

# UnitType admin
class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_custom', 'is_archived')
    search_fields = ('name',)
    list_filter = ('is_custom', 'is_archived')

custom_admin_site.register(UnitType, UnitTypeAdmin)

# UnitImage admin
class UnitImageAdmin(admin.ModelAdmin):
    list_display = ('unit', 'unit_template', 'image_type', 'uploaded_at', 'image_preview')
    list_filter = ('image_type', 'uploaded_at')
    search_fields = ('unit__unit_title', 'unit_template__name')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Preview'

custom_admin_site.register(UnitImage, UnitImageAdmin)
