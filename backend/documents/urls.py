from django.urls import path
from . import views

urlpatterns = [
    path('document-types/', views.DocumentTypeListView.as_view(), name='document-type-list'),  # Listing and creating document types
    path('document-types/<int:pk>/', views.DocumentTypeDetailView.as_view(), name='document-type-detail'),  # Viewing, updating, and deleting a single document type
    path('', views.DocumentListCreateView.as_view(), name='document-list-create'),  # Listing and creating documents
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),  # Viewing a single document
]
