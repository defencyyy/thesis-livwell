from rest_framework import serializers
from .models import Customer
from brokers.models import Broker
from brokers.serializers import DeveloperBrokerSerializer
from documents.serializers import DocumentSerializer
from units.serializers import UnitSerializer  # Adjust import based on your structure
from sites.serializers import SiteSerializer  # Adjust import based on your structure

class CustomerSaleSerializer(serializers.Serializer):
    """Detailed representation of a sale."""
    id = serializers.IntegerField()
    status = serializers.CharField()
    reservation_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit = UnitSerializer()  # Serialize unit details
    site = SiteSerializer()  # Serialize site details

class CustomerSerializer(serializers.ModelSerializer):
    broker = DeveloperBrokerSerializer(read_only=True)
    documents = serializers.SerializerMethodField()
    broker_sales = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_documents(self, obj):
        documents = obj.documents.all()
        return DocumentSerializer(documents, many=True).data

    def get_broker_sales(self, obj):
        from sales.models import Sale  # Avoid circular import issues
        sales = (
            Sale.objects.filter(customer=obj)
            .select_related('unit__site')  # Optimize query to include related data
            .values('id', 'status', 'reservation_fee', 'unit__id', 'unit__unit_title', 'unit__status', 'unit__site__name')  # Changed unit__title to unit__unit_title
        )

        # Map the query results to match the structure expected by the frontend
        return [
            {
                "id": sale["id"],
                "status": sale["status"],
                "reservation_fee": sale["reservation_fee"],
                "unit": {
                    "id": sale["unit__id"],
                    "title": sale["unit__unit_title"],  # Changed unit__title to unit__unit_title
                    "status": sale["unit__status"],
                },
                "site": {
                    "name": sale["unit__site__name"],
                },
            }
            for sale in sales
        ]




class EditCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'broker']

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_number']
