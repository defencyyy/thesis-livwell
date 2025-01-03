from django.urls import path
from .views import SaleListView, SaleDetailView, SalesStatusByYearView

urlpatterns = [
    path('', SaleListView.as_view(), name='sales-list'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('status/<int:year>/', SalesStatusByYearView.as_view(), name='sales_status_by_year'),]
