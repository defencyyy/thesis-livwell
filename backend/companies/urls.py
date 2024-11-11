from django.urls import path
from .views import CompanyView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',  csrf_exempt(CompanyView.as_view()), name='company'), 
]
