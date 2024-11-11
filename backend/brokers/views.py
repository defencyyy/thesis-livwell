from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Broker
from .serializers import BrokerSerializer
import logging
from developers.models import Developer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Set up logging
logger = logging.getLogger(__name__)

class BrokerListView(APIView):
    def get(self, request):
        """Handle GET request to list brokers."""
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        logger.debug(f"GET request received with Developer-ID: {developer_id} and Company-ID: {company_id}")

        if not developer_id or not company_id:
            logger.error("Developer ID or Company ID not provided")
            return Response({'error': 'Developer ID or Company ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch developer to ensure they are associated with the company
            developer = Developer.objects.get(id=developer_id)
            if developer.company.id != int(company_id):
                logger.warning("Unauthorized access attempt")
                return Response({'error': 'Unauthorized access to brokers'}, status=status.HTTP_401_UNAUTHORIZED)

            # Fetch brokers associated with the developer's company
            brokers = Broker.objects.filter(company_id=company_id)
            serializer = BrokerSerializer(brokers, many=True)

            return Response(serializer.data)

        except Developer.DoesNotExist:
            logger.error("Developer not found")
            return Response({'error': 'Developer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching brokers: {str(e)}")
            return Response({'error': 'Error fetching brokers'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BrokerCreateView(APIView):
    @csrf_exempt
    def post(self, request):
        """Handle POST request to create a broker."""
        try:
            data = json.loads(request.body)
            
            # Ensure that data is complete
            required_fields = ['company_id', 'email', 'contact_number', 'last_name', 'first_name', 'password']
            if not all(field in data for field in required_fields):
                return JsonResponse({"success": False, "message": "Missing required fields"}, status=400)

            # Create the new broker entry
            broker = Broker.objects.create(
                company_id=data['company_id'],
                email=data['email'],
                contact_number=data.get('contact_number', ''),  # Default to empty if not provided
                last_name=data['last_name'],
                first_name=data['first_name'],
                password=data['password']  # Ensure password is handled securely
            )

            # Return a success response
            return JsonResponse({"success": True, "message": "Broker added successfully!"}, status=201)

        except Exception as e:
            logger.error(f"Error creating broker: {str(e)}")
            return JsonResponse({"success": False, "message": str(e)}, status=500)
