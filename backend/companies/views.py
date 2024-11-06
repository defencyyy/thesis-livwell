import logging
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
        logging.debug(f"Request user: {request.user}, Authenticated: {request.user.is_authenticated}")

        # Check if request.user is set correctly
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            logging.error("User ID not found in request.user.")
            return Response({"error": "User authentication failed."}, status=status.HTTP_403_FORBIDDEN)

        try:
            developer = Developer.objects.get(id=user_id)
            logging.debug(f"Developer found: {developer}")
        except Developer.DoesNotExist:
            logging.error("Developer does not exist.")
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the developer has an associated company
        if not hasattr(developer, 'company'):
            logging.error("Developer has no associated company.")
            return Response({"error": "Developer has no associated company"}, status=status.HTTP_404_NOT_FOUND)

        company = developer.company
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request):
        user_id = getattr(request.user, 'id', None)
        if not user_id:
            logging.error("User ID not found in request.user.")
            return Response({"error": "User authentication failed."}, status=status.HTTP_403_FORBIDDEN)

        try:
            developer = Developer.objects.get(id=user_id)
            logging.debug(f"Developer found: {developer}")
        except Developer.DoesNotExist:
            logging.error("Developer does not exist.")
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the developer has an associated company
        if not hasattr(developer, 'company'):
            logging.error("Developer has no associated company.")
            return Response({"error": "Developer has no associated company"}, status=status.HTTP_404_NOT_FOUND)

        company = developer.company
        serializer = CompanySerializer(company, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
