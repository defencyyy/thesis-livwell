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

from django.db.models import Count
from .models import Sale, Site

def top_sites_sale_count():
    # Count the number of sales per site and order by the count in descending order
    top_sites = (Sale.objects
                 .values('site')  # Group by site
                 .annotate(sale_count=Count('id'))  # Count the sales
                 .order_by('-sale_count')  # Order by the count in descending order
                 [:5])  # Get top 5 sites

    # Get the site names and sales counts
    data = []
    for site in top_sites:
        site_name = Site.objects.get(id=site['site']).name  # Assuming Site has a name field
        data.append({
            'site': site_name,
            'sales': site['sale_count'],
        })
    
    return data

from django.http import JsonResponse
from django.db.models import Count
from .models import Sale
from datetime import datetime

def sales_status_by_year(request, year):
    sales_status_counts = (
        Sale.objects.filter(date_sold__year=year)
        .values('status')
        .annotate(count=Count('status'))
        .order_by('status')
    )
    return JsonResponse({'data': list(sales_status_counts)})
