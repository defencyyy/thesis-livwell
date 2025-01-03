from django.urls import path
from .views import CompanyDetailView, CompanyUpdateView

urlpatterns = [
    path('', CompanyDetailView.as_view(), name='company-detail'),
    path('edit/', CompanyUpdateView.as_view(), name='company-update'),
]
