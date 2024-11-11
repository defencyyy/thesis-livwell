from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Broker
from django.contrib.auth.hashers import make_password

class BrokerAdmin(admin.ModelAdmin):
    broker_display = ('id', 'company', 'username', 'email', 'contact_number', 'first_name', 'last_name') 
    broker_display_links = ('id', 'username') 
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company__name') 
    broker_per_page = 25

    # Override the save_model method to set a default password if none is provided
    def save_model(self, request, obj, form, change):
        # If no password is provided, set it to 'username.12345'
        if not obj.password:
            obj.password = f"{obj.username}.12345" 
            
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(Broker, BrokerAdmin)
