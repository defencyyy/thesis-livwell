from django.urls import path
from .views import EditCompany

urlpatterns = [
    path('', EditCompany, name="company-view-edit"), 
]
