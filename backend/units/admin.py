from django.contrib import admin
from django.utils.html import mark_safe
from .models import Unit, UnitImage, UnitTemplate
from prbe.admin import custom_admin_site
from django import forms

# UnitTemplate Admin
class UnitTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'name', 'bedroom', 'bathroom', 'floor_area', 'lot_area', 'price', 'view', 'balcony', 'commission', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_filter = ('view', 'balcony')
    ordering = ('name',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        # Optionally add any additional logic during saving
        super().save_model(request, obj, form, change)

custom_admin_site.register(UnitTemplate, UnitTemplateAdmin)

# UnitImage Inline
class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1  # Shows one empty form by default for adding new images
    fields = ['image', 'uploaded_at', 'image_preview', 'image_type', 'unit', 'unit_template']
    readonly_fields = ['uploaded_at', 'image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'


# UnitAdmin to show inline for images
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
    list_display = ('unit', 'unit_template', 'image_type', 'image', 'uploaded_at', 'image_preview')
    search_fields = ('unit__unit_title', 'unit_template__name')
    list_filter = ('uploaded_at', 'image_type', 'unit', 'unit_template')

    # Form to show the dropdown options correctly
    class UnitImageForm(forms.ModelForm):
        class Meta:
            model = UnitImage
            fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # If unit is selected, disable unit_template field and vice versa
            if self.instance and self.instance.image_type == 'unit':
                self.fields['unit_template'].queryset = UnitTemplate.objects.none()
            if self.instance and self.instance.image_type == 'unit_template':
                self.fields['unit'].queryset = Unit.objects.none()

    form = UnitImageForm

    # Define the image preview method inside UnitImageAdmin
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'


custom_admin_site.register(UnitImage, UnitImageAdmin)
