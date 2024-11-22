from django.urls import path
from .views import SiteListView, SiteDetailView

urlpatterns = [
    path('', SiteListView.as_view(), name='view-site'),
    path('add/', SiteListView.as_view(), name='add-site'),  
    path('<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
]
