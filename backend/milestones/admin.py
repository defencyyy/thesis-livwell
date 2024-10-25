from django.contrib import admin
from .models import Milestone

class MilestoneAdmin(admin.ModelAdmin):
  milestone_display = ('id', 'name', 'reward', 'type', 'created_at')  
  milestone_display_links = ('id', 'name')  
  search_fields = ('name', 'description', 'reward')
  milestone_per_page = 25 

admin.site.register(Milestone, MilestoneAdmin)
