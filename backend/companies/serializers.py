from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
  class Meta:
    model = Company
    fields = ['name', 'description', 'logo', 'is_active', 'created_at', 'updated_at']
    read_only_fields = ['name', 'created_at', 'updated_at', 'is_active']