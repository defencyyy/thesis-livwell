from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
  customer_display = ('id', 'company', 'name', 'email', 'contact_number')
  customer_display_links = ('id', 'name')
  search_fields = ('name', 'company', 'email', 'username', 'description')
  customer_per_page = 25

admin.site.register(Customer, CustomerAdmin)