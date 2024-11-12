from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from .models import Broker
from .serializers import BrokerSerializer
import logging
from developers.models import Developer

# Set up logging
logger = logging.getLogger(__name__)

class BrokerView(APIView):
    # Only use Token Authentication
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        # Get company_id from the request headers or query parameters
        company_id = request.headers.get('Company-ID') or request.query_params.get('company_id')
        
        if not company_id:
            return Response({"detail": "Company ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter brokers by company ID
        brokers = Broker.objects.filter(company_id=company_id)
        serializer = BrokerSerializer(brokers, many=True)
        return Response({"brokers": serializer.data}, status=status.HTTP_200_OK)

class BrokerCreateView(APIView):
    # Only use Token Authentication
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Get company_id from the request headers or body (query params or form data)
        company_id = request.headers.get('Company-ID') or request.data.get('company_id')
        
        if not company_id:
            return Response({"detail": "Company ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Attach the company_id to the broker data before validation
        data = request.data.copy()
        data['company_id'] = company_id

        # Validate and save the broker data
        serializer = BrokerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Broker added successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
