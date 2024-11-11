from rest_framework import serializers
from .models import Broker

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = ['email', 'username', 'first_name', 'last_name', 'contact_number', 'password', 'company']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False}
        }

    def validate_email(self, value):
        if Broker.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_username(self, value):
        if Broker.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")
        return value
