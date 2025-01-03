from django.urls import path
from .views import CustomerListView, CustomerDetailView, CustomerDocumentListView

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-view'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('<int:customer_id>/documents/', CustomerDocumentListView.as_view(), name='customer-documents'),
]