from rest_framework import serializers
from .models import Broker

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['email', 'username', 'first_name', 'last_name', 'contact_number', 'password', 'company']
        extra_kwargs = {
            'password': {'write_only': True}
        }
