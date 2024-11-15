from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from developers.models import Developer
from companies.models import Company
from .serializers import CompanySerializer

class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the Developer associated with the logged-in user
            developer = Developer.objects.get(id=request.user.id)
            company = developer.company
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

class CompanyUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Retrieve the developer_id from the request
        developer_id = request.data.get("developer_id")
        
        # Validate if the developer_id matches the logged-in user
        if developer_id != request.user.id:
            return Response({"error": "You are not authorized to update this company."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            # Get the Developer based on the logged-in user (if the ID matches)
            developer = Developer.objects.get(id=request.user.id)
            company = developer.company

            # Ensure the developer_id from the request matches the developer
            if company.developer.id != developer_id:
                return Response({"error": "Developer ID mismatch."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Proceed to update company details
            serializer = CompanySerializer(company, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)