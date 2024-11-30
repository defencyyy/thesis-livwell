from rest_framework import serializers
from customers.serializers import CustomerSerializer  # Import CustomerSerializer
from brokers.serializers import DeveloperBrokerSerializer  # Import BrokerSerializer
from sites.serializers import SiteSerializer
from units.serializers import UnitSerializer
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()  # Use CustomerSerializer
    broker = DeveloperBrokerSerializer()  # Use BrokerSerializer
    site = SiteSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Sale
        fields = ['id', 'customer', 'broker', 'unit', 'site', 'status', 'reservation_fee', 'payment_method', 'reservation_file']