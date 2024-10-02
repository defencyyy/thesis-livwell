from django.contrib import admin
from .models import Broker

class BrokerAdmin(admin.ModelAdmin):
  broker_display = ('id', 'company', 'name', 'affiliations', 'email', 'contact_number')
  broker_display_links = ('id', 'name')
  search_fields = ('name', 'company', 'email', 'username', 'affiliations', 'description')
  broker_per_page = 25

admin.site.register(Broker, BrokerAdmin)