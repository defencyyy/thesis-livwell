from rest_framework import serializers
from .models import Document, DocumentType
from companies.models import Company
from customers.models import Customer
from sales.models import Sale

# Serializer for DocumentType
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description']

# Serializer for Document
class DocumentSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer()
    company_name = serializers.CharField(source='company.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    sales_id = serializers.IntegerField(source='sales.id', read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'company', 'customer', 'description', 'file', 'uploaded_at', 'document_type', 'company_name', 'customer_name', 'sales_id']
