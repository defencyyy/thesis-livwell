from rest_framework import serializers
from .models import Customer
from brokers.models import Broker
from brokers.serializers import DeveloperBrokerSerializer

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    broker = DeveloperBrokerSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

class EditCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'contact_number', 'broker']


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['id', 'first_name', 'last_name', 'email', 'contact_number']
