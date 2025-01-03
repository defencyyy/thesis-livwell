from django.urls import path
from . import views

urlpatterns = [
    path('', views.MilestoneListCreateView.as_view(), name='milestone-list-create'),  # Listing and creating milestones
    path('<int:pk>/', views.MilestoneDetailView.as_view(), name='milestone-detail'),  # Viewing, updating, and deleting a single milestone
]
