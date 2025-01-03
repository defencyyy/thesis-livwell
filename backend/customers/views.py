from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from developers.models import Developer
from .models import Customer
from .serializers import CustomerSerializer, EditCustomerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from documents.models import Document
from documents.serializers import DocumentSerializer

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Fetch the developer's company
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Retrieve the archived filter from query params (default to 'false')
            archived = request.query_params.get('archived', 'false').lower() in ['true', '1']

            # Filter customers based on the archived status
            customers = Customer.objects.filter(company=company, archived=archived)
            serializer = CustomerSerializer(customers, many=True)

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        try:
            # Fetch the developer's company
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Associate the company with the customer being created
            data = request.data
            data['company'] = company.id
            serializer = CustomerSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Fetch the developer's company
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Retrieve the customer if they belong to the developer's company
            customer = Customer.objects.get(id=pk, company=company)
            serializer = CustomerSerializer(customer)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk):
        try:
            # Fetch the developer's company
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Retrieve the customer if they belong to the developer's company
            customer = Customer.objects.get(id=pk, company=company)
            serializer = EditCustomerSerializer(customer, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            # Fetch the developer's company
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Retrieve the customer if they belong to the developer's company
            customer = Customer.objects.get(id=pk, company=company)
            customer.delete()

            return Response({"message": "Customer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class CustomerDocumentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        # Get the customer object
        customer = get_object_or_404(Customer, id=customer_id)

        # Assuming the customer has a related documents model
        documents = Document.objects.filter(customer=customer)
        serializer = DocumentSerializer(documents, many=True)

        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
