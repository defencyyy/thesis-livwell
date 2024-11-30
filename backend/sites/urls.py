from django.urls import path
from .views import SiteListView, SiteDetailView, StatusOptionsView
from .location import get_location_data

urlpatterns = [
    path('', SiteListView.as_view(), name='site-main'),
    path('<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('locations/', get_location_data, name='get_location_data'),
    path('status-options/', StatusOptionsView.as_view(), name='status-options'),
]