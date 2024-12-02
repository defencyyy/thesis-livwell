from rest_framework import generics
from .models import Document, DocumentType
from .serializers import DocumentSerializer, DocumentTypeSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# View to list and create Document Types
class DocumentTypeListView(generics.ListCreateAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Custom logic can be added if needed
        serializer.save()

# View to retrieve, update, or delete a Document Type
class DocumentTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticated]

# View to list and create Documents
class DocumentListCreateView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the document with the user or company, if necessary
        serializer.save(company=self.request.user.company)

    def get_queryset(self):
        # Optionally filter documents by user or company
        return Document.objects.filter(company=self.request.user.company)

# View to retrieve, update, or delete a Document
class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
