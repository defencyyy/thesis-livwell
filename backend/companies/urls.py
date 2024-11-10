from django.urls import path
from .views import CompanyView

urlpatterns = [
    path('developer/company/', CompanyView.as_view(), name='company'),
]
