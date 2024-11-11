from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Broker
from .serializers import BrokerSerializer
import logging

# Set up logging
logger = logging.getLogger(__name__)

class BrokerView(APIView):

    def get(self, request):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')
        
        logger.debug(f"GET request received with Developer-ID: {developer_id} and Company-ID: {company_id}")

        if not developer_id or not company_id:
            logger.error("Developer ID or Company ID not provided")
            return Response({'error': 'Developer ID or Company ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Assuming Developer model is linked to the Company model
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


    def post(self, request):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')
        
        logger.debug(f"POST request received with Developer-ID: {developer_id} and Company-ID: {company_id}")

        if not developer_id or not company_id:
            logger.error("Developer ID or Company ID not provided")
            return Response({"message": "Developer ID or Company ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the developer is associated with the company
            developer = Developer.objects.get(id=developer_id)
            if developer.company.id != int(company_id):
                logger.warning("Unauthorized access attempt")
                return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

            # Gather broker data from the request
            broker_data = {
                "company_id": company_id,
                "email": request.data.get("email"),
                "username": request.data.get("username"),
                "last_name": request.data.get("last_name"),
                "first_name": request.data.get("first_name"),
                "contact_number": request.data.get("contact_number", ""),
                "password": request.data.get("password", "12345")
            }
            broker_serializer = BrokerSerializer(data=broker_data)

            if broker_serializer.is_valid():
                broker_serializer.save()
                return Response({"message": "Broker created successfully!"}, status=status.HTTP_201_CREATED)
            return Response(broker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Developer.DoesNotExist:
            logger.error("Developer not found")
            return Response({"message": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error creating broker: {e}")
            return Response({"message": "An error occurred while creating the broker"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
