from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Company
from developers.models import Developer
from .serializers import CompanySerializer
from rest_framework import status

class CompanyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        developer_id = request.user.id

        print(f"Request user ID: {request.user.id}")  # Debugging line

        try:
            developer = Developer.objects.get(id=developer_id)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not hasattr(developer, 'company'):
            return Response({"error": "Developer has no associated company"}, status=status.HTTP_404_NOT_FOUND)
        
        company = developer.company
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request):
        developer_id = request.user.id

        try:
            developer = Developer.objects.get(id=developer_id)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not hasattr(developer, 'company'):
            return Response({"error": "Developer has no associated company"}, status=status.HTTP_404_NOT_FOUND)

        company = developer.company
        serializer = CompanySerializer(company, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
