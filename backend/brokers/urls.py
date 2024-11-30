from django.urls import path
from .views import BrokerListView, BrokerDetailView, ArchivedBrokerView

urlpatterns = [
    path('', BrokerListView.as_view(), name='view-broker'), 
    path('add/', BrokerListView.as_view(), name='add-broker'),  
    path('<int:pk>/', BrokerDetailView.as_view(), name='edit-broker'), 
    path('archived/', ArchivedBrokerView.as_view(), name='view-archived'),
    path('archived/<int:pk>/', ArchivedBrokerView.as_view(), name='unarchive-broker'),
]
