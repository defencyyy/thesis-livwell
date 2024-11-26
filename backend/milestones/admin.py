from django.contrib import admin
from .models import Milestone
from prbe.admin import custom_admin_site

class MilestoneAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'reward', 'type', 'created_at') 
  list_display_links = ('id', 'name') 
  search_fields = ('name', 'description', 'reward')  
  list_per_page = 25  

custom_admin_site.register(Milestone, MilestoneAdmin) 