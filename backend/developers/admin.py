from django.contrib import admin
from .models import Developer

class DeveloperAdmin(admin.ModelAdmin):
  developer_display = ('id', 'company', 'name', 'email', 'contact_number')
  developer_display_links = ('id', 'name')
  search_fields = ('name', 'company', 'email', 'username', 'description')
  developer_per_page = 25

admin.site.register(Developer, DeveloperAdmin)