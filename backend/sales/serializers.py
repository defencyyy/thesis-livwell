from rest_framework import serializers
from .models import Sale
from brokers.serializers import DeveloperBrokerSerializer
from sites.serializers import SiteSerializer
from units.serializers import UnitSerializer


class SaleCustomerSerializer(serializers.Serializer):
    """Minimal representation of a customer to avoid circular imports."""
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class SaleSerializer(serializers.ModelSerializer):
    customer = SaleCustomerSerializer()  # Use minimal customer representation
    broker = DeveloperBrokerSerializer()
    site = SiteSerializer()
    unit = UnitSerializer()

    class Meta:
        model = Sale
        fields = ['id', 'customer', 'broker', 'unit', 'site', 'status', 'reservation_fee', 'payment_method', 'reservation_file']
