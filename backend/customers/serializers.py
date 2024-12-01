from rest_framework import serializers
from .models import Customer
from brokers.models import Broker
from brokers.serializers import DeveloperBrokerSerializer
from documents.serializers import DocumentSerializer, DocumentTypeSerializer

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    broker = DeveloperBrokerSerializer(read_only=True)
    documents = serializers.SerializerMethodField()  # Method to fetch documents

    class Meta:
        model = Customer
        fields = '__all__'

    def get_documents(self, obj):
        from documents.models import Document
        from documents.serializers import DocumentSerializer

        # Retrieve related documents
        documents = obj.documents.all()  # Use the related_name `documents`
        serialized_documents = DocumentSerializer(documents, many=True).data
        
        # Debug output to log the serialized data
        print("Related Documents for Customer ID:", obj.id)
        print(serialized_documents)
        
        return serialized_documents

class EditCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'broker']

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_number']
