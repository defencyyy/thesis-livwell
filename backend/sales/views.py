from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Sale
from .serializers import SaleSerializer

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

        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        sales = Sale.objects.filter(company=company)
        serializer = SaleSerializer(sales, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

class SaleDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )
       
        sale = get_object_or_404(Sale, pk=pk, company=company)
        serializer = SaleSerializer(sale)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
