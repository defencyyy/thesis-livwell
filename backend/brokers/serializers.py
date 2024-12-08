from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Broker

class DeveloperBrokerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make sure the password is write-only
    total_sales = serializers.ReadOnlyField()
    total_commissions = serializers.ReadOnlyField()

    class Meta:
        model = Broker
        fields = ['id', 'company', 'email', 'username', 'contact_number', 'first_name', 'last_name', 'password', 'archived', 'total_sales', 'total_commissions']
        extra_kwargs = {
            'username': {'required': False},  # Allow username to be set later
        }

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email'].split('@')[0]  # Example: use the email's local part as username

        # Hash the password before creating the Broker instance
        password = validated_data.pop('password')  # Remove password from validated data
        hashed_password = make_password(password)  # Hash the password
        validated_data['password'] = hashed_password  # Add the hashed password back into the validated data
        
        # Create the Broker instance with the validated data (including hashed password)
        return super().create(validated_data)

class EditBrokerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Optional password for editing

    class Meta:
        model = Broker
        fields = ['company', 'email', 'username', 'contact_number', 'first_name', 'last_name', 'password', 'archived']
        read_only_fields = ['company']

    def update(self, instance, validated_data):
        # If password is provided, hash it before saving
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)  # Hash the new password before saving

        # Update other fields
        return super().update(instance, validated_data)
