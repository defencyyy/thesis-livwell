# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Company

# Assuming you have a Developer model related to the User model
from .serializers import CompanySerializer

@api_view(['GET', 'PUT'])
def EditCompany(request):
    # Get the logged-in developer's company
    try:
        company = request.user.developer.company  # Ensure that the user has a developer instance
    except AttributeError:
        return Response({"error": "Developer not found for this user"}, status=status.HTTP_404_NOT_FOUND)
    except Company.DoesNotExist:
        return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
