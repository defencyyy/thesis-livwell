from rest_framework import serializers
from .models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'id', 'site', 'unit', 'customer', 'broker', 'company', 'date_sold', 'status',
            'reservation_fee', 'payment_method', 'payment_reference', 'reservation_file'
        ]
