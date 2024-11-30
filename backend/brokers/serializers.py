from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Broker

class DeveloperBrokerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make sure the password is write-only

    class Meta:
        model = Broker
        fields = ['id', 'company', 'email', 'username', 'contact_number', 'first_name', 'last_name', 'password', 'archived']
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


# editing own acc (broker)
# class BrokerSelfEditSerializer(serializers.ModelSerializer):
#     # Ensure password is hashed before saving
#     password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = Broker
#         fields = ['id', 'email', 'username', 'contact_number', 'password']

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         if password:
#             instance.password = make_password(password)
#         return super().update(instance, validated_data)
