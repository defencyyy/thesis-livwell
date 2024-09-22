from django.contrib import admin
from .models import Property

class PropertyAdmin(admin.ModelAdmin):
  property_display = ('id', 'title', 'is_active', 'is_listed', 'price', 'post_date',)
  property_display_links = ('id', 'title')
  property_filter = ('city',)
  property_editable = ('is_active', 'is_listed')
  search_fields = ('title', 'description', 'address', 'city', 'price')
  list_per_page = 25
  
admin.site.register(Property, PropertyAdmin)