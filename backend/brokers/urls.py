from django.urls import path
from .views import BrokerListView, BrokerDetailView

urlpatterns = [
    path('', BrokerListView.as_view(), name='view-broker'),  # List brokers
    path('add/', BrokerListView.as_view(), name='add-broker'),  # Edit specific broker
    path('<int:pk>/', BrokerDetailView.as_view(), name='edit-broker'),  # Edit specific broker
]
