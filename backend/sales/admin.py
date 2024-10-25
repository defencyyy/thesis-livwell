from django.contrib import admin
from .models import Sale

class SaleAdmin(admin.ModelAdmin):
  sales_display = ('id', 'site', 'unit', 'customer', 'broker', 'date_sold')  
  sales_display_links = ('id', 'customer')  
  search_fields = ('name', 'unit', 'customer', 'broker', 'date_sold')
  sales_per_page = 25 

admin.site.register(Sale, SaleAdmin)