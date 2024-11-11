from django.urls import path
from .views import BrokerView

urlpatterns = [
    path('create/', BrokerView.as_view(), name='create-broker'),  # Endpoint for creating brokers
    path('', BrokerView.as_view(), name='get-brokers'),  # Endpoint for listing brokers
]
