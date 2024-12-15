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

    def validate_username(self, value):
        """Ensure that the username doesn't contain any spaces."""
        if ' ' in value:
            raise serializers.ValidationError("Username must not contain spaces.")
        return value

    def create(self, validated_data):
        if 'username' not in validated_data:
            # Remove spaces from first_name before generating the username
            first_name = validated_data.get('first_name', '').replace(' ', '')
            last_name = validated_data.get('last_name', '').replace(' ', '')
            validated_data['username'] = f"{validated_data['email'].split('@')[0]}{first_name}{last_name}".lower()  # Example: email local part + first_name + last_name

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


# The post method that handles the automatic generation of the username
def post(self, request):
    try:
        developer = Developer.objects.get(id=request.user.id)

        if not hasattr(developer, 'company'):
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

        company = developer.company

        data = request.data
        data['company'] = company.id

        serializer = DeveloperBrokerSerializer(data=data)

        if serializer.is_valid():
            broker = serializer.save()

            # Automatically create the username by removing spaces from first_name
            broker.username = f"{broker.id}.{broker.first_name.replace(' ', '')}{broker.last_name.replace(' ', '')}".lower()
            broker.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Developer.DoesNotExist:
        return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
