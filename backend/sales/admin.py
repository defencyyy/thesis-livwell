from django.contrib import admin
from .models import Sale
from prbe.admin import custom_admin_site

class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'unit', 'customer', 'broker', 'status', 'date_sold', 'reservation_fee', 'payment_method')
    list_display_links = ('id', 'customer')
    list_filter = ('status', 'payment_method', 'site', 'date_sold')
    search_fields = ('unit__unit_title', 'customer__first_name', 'customer__last_name', 'broker__first_name', 'broker__last_name', 'payment_reference')
    list_per_page = 25
    
    # Read-only fields
    readonly_fields = ('date_sold', 'company', 'site')  
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'date_sold', 'site', 'unit', 'customer', 'broker', 'status',)
        }),
        ('Payment Details', {
            'fields': ('reservation_fee', 'payment_method', 'payment_reference')
        }),
        ('Reservation File', {
            'fields': ('reservation_file',)
        }),
    )

custom_admin_site.register(Sale, SaleAdmin)
