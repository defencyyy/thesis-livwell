from django.urls import path
from .views import SiteListView, SiteDetailView

urlpatterns = [
    path('', SiteListView.as_view(), name='site-main'),
    path('<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
]
