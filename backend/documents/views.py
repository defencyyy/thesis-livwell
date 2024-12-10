from rest_framework import generics
from .models import Document, DocumentType
from .serializers import DocumentSerializer, DocumentTypeSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q  # Importing Q for complex queries

# Function to get the developer's company
def get_developer_company(request):
    developer = request.user
    if not hasattr(developer, 'company'):
        return None
    return developer.company

# View to list and create Document Types, filtering by the user's company
class DocumentTypeListView(generics.ListCreateAPIView):
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the developer's company
        company = get_developer_company(self.request)
        if not company:
            return DocumentType.objects.none()  # Return no results if no company found
        # Filter DocumentTypes by the user's company
        return DocumentType.objects.filter(company=company)

    def perform_create(self, serializer):
        # Add the company to the document type when creating
        company = get_developer_company(self.request)
        if company:
            serializer.save(company=company)

# View to retrieve, update, or delete a Document Type, ensuring it's from the developer's company
class DocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the developer's company
        company = get_developer_company(self.request)
        if not company:
            return DocumentType.objects.none()  # Return no results if no company found
        # Filter DocumentType by company
        return DocumentType.objects.filter(company=company)

# View to list and create Documents, ensuring they are associated with the developer's company
class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the developer's company
        company = get_developer_company(self.request)
        if not company:
            return Document.objects.none()  # Return no results if no company found
        # Filter Documents by the user's company
        return Document.objects.filter(company=company)

    def perform_create(self, serializer):
        # Associate the document with the user's company
        company = get_developer_company(self.request)
        if company:
            serializer.save(company=company)

# View to retrieve, update, or delete a Document, ensuring it belongs to the developer's company
class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the developer's company
        company = get_developer_company(self.request)
        if not company:
            return Document.objects.none()  # Return no results if no company found
        # Filter Document by company
        return Document.objects.filter(company=company)

    def perform_update(self, serializer):
        # Ensure the document remains associated with the user's company during updates
        company = get_developer_company(self.request)
        if company:
            serializer.save(company=company)
