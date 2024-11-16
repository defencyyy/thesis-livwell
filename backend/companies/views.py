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
        try:
            # Get the Developer associated with the logged-in user
            developer = Developer.objects.get(id=request.user.id)

            # Ensure the developer has an associated company
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            print("Received data:", request.data)
            if "logo" in request.FILES:
                print("Logo file:", request.FILES["logo"])

            # Update the company details using the serializer
            serializer = CompanySerializer(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
