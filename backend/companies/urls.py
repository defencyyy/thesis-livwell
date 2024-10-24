from django.urls import path
from .views import CompanyView

urlpatterns = [
    path('', CompanyView.as_view(), name='company_list'),  # For GET, POST
    path('<int:pk>/', CompanyView.as_view(), name='company_detail'),  # For GET, PUT, DELETE
]
