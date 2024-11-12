from django.urls import path
from .views import BrokerView, BrokerCreateView

urlpatterns = [
    path('', BrokerView.as_view(), name='get-brokers'),  # For GET request to list brokers
    path('create/', BrokerCreateView.as_view(), name='create-broker'),  # For POST request to create a broker
]
