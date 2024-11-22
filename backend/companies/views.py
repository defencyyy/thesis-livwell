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

            # Print the data and files received in the request for debugging
            print("Received data:", request.data)
            print("Received files:", request.FILES)

            # Update the company details using the serializer
            serializer = CompanySerializer(company, data=request.data, partial=True)

            # Check if files are included and update the company logo separately
            if 'logo' in request.FILES:
                company.logo = request.FILES['logo']
                print(f"Logo file received: {company.logo.name}")

            if serializer.is_valid():
                # Save the company instance after validating
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            print(serializer.errors)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log and return other errors
            print(f"Error: {str(e)}")
            return Response({"error": "An error occurred while updating company."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
