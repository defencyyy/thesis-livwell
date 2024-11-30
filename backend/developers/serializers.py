from rest_framework import serializers
from django.contrib.auth import get_user_model

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'contact_number', 'first_name', 'last_name', 'password']
