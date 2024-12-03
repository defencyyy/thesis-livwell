from django.contrib import admin
from .models import Broker
from prbe.admin import custom_admin_site  # Assuming custom admin site is being used

# Broker Admin
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'username', 'email', 'contact_number', 'first_name', 'last_name', 'archived', 'total_sales', 'total_commissions') 
    list_display_links = ('id', 'username') 
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company__name')  # Enable searching by company name
    list_per_page = 25

    # Adding custom methods for total sales and total commissions
    def total_sales(self, obj):
        return obj.total_sales  # Calls the `total_sales` property of Broker model
    total_sales.admin_order_field = 'total_sales'
    total_sales.short_description = 'Total Sales'

    def total_commissions(self, obj):
        return obj.total_commissions  # Calls the `total_commissions` property of Broker model
    total_commissions.admin_order_field = 'total_commissions'
    total_commissions.short_description = 'Total Commissions'

custom_admin_site.register(Broker, BrokerAdmin)
