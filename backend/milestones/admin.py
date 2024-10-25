from django.contrib import admin
from .models import Milestone

class MilestoneAdmin(admin.ModelAdmin):
  Milestone_display = ('id', 'name', 'reward', 'type', 'created_at')  
  Milestone_display_links = ('id', 'name')  
  search_fields = ('name', 'description', 'reward')
  Milestone_per_page = 25 

admin.site.register(Milestone, MilestoneAdmin)