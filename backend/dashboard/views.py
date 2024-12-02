from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from brokers.models import Broker
from sales.models import Sale
from sites.models import Site
from units.models import Unit

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            company = request.user.company  # Get the company associated with the authenticated user

            # Broker count (active brokers only)
            brokers_count = Broker.objects.filter(company=company, archived=False).count()

            # Site count (active sites only)
            sites_count = Site.objects.filter(company=company, archived=False).count()

            # Available Units count (not sold, not archived, and active)
            available_units_count = Unit.objects.filter(
                company=company, 
                status__in=['available', 'pending reservation'],
            ).count()

            # Sales count (sold sales only)
            sales_count = Sale.objects.filter(company=company, status='Sold').count()

            # Ongoing Sales count (sales that are in progress)
            ongoing_sales_count = Sale.objects.filter(
                company=company, 
                status__in=['Pending Reservation', 'Reserved', 'Pending Sold']
            ).count()

            # Return the data as response
            return Response({
                "brokers": brokers_count,
                "sites": sites_count,
                "availableUnits": available_units_count,
                "salesCount": sales_count,
                "ongoingSales": ongoing_sales_count
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"error": "An error occurred while fetching stats."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
