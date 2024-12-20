import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Sale
from .serializers import SaleSerializer

# Set up logging
logger = logging.getLogger(__name__)

def get_developer_company(request):
    """
    Helper function to get the company of the logged-in developer.
    """
    developer = request.user
    print(f"Developer: {developer}, Company: {developer.company}")
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

        # Use Q to filter sales for the company
        sales = Sale.objects.filter(Q(company=company))
        serializer = SaleSerializer(sales, many=True)

        # Log the sales data being returned
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

        # Log fetched sale details
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
        
        # Log incoming PUT request data
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

from django.http import JsonResponse
from django.db.models import Count
from .models import Sale

class SalesStatusByYearView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request, year):
        # Try to get the company associated with the logged-in user
        company = get_developer_company(request)

        # If no company is associated with the user, return an error or empty data
        if not company:
            return JsonResponse({'message': 'No company available for the user'}, status=400)

        # Start building the filter with date_sold year
        filters = {'date_sold__year': year, 'company_id': company.id}

        # Query Sale objects based on the filters
        sales_status_counts = (
            Sale.objects.filter(**filters)  # Apply the filters dynamically
            .values('status')
            .annotate(count=Count('status'))
            .order_by('status')
        )

        # Return the data in a response
        return Response({'data': list(sales_status_counts)}, status=status.HTTP_200_OK)