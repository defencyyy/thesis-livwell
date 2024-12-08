import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Sale
from .serializers import SaleSerializer

# Set up logging
logger = logging.getLogger(__name__)

def get_developer_company(request):
    """
    Helper function to get the company of the logged-in developer.
    """
    developer = request.user
    if not hasattr(developer, 'company'):
        return None
    return developer.company

class SaleListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get developer's company
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch sales for the company
        sales = Sale.objects.filter(company=company)
        serializer = SaleSerializer(sales, many=True)
        
        # Log sales data
        logger.debug(f"Sales data fetched for company: {company.name}. Sales: {serializer.data}")
        
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

class SaleDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Get developer's company
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Fetch sale by ID and company
        sale = get_object_or_404(Sale, pk=pk, company=company)
        serializer = SaleSerializer(sale)
        
        # Log fetched sale data
        logger.debug(f"Sale details fetched: {serializer.data}")
        
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Get developer's company
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fetch the sale to update
        sale = get_object_or_404(Sale, pk=pk, company=company)
        
        # Log the incoming PUT request data for debugging
        logger.debug(f"Incoming PUT request data for Sale ID {pk}: {request.data}")
        
        # Extract status from request data
        status_value = request.data.get('status')
        
        if status_value:
            # Update sale status
            sale.status = status_value
            sale.save()
            logger.debug(f"Sale status updated to: {sale.status} for Sale ID {pk}")
            
            # Serialize the updated sale
            serializer = SaleSerializer(sale)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            # Log missing status in PUT request
            logger.warning(f"No 'status' provided in PUT request for Sale ID {pk}.")
            return Response({"error": "Status not provided."}, status=status.HTTP_400_BAD_REQUEST)