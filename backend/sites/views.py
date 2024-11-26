import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from developers.models import Developer
from .models import Site
from .serializers import SiteSerializer

# Set up logging
logger = logging.getLogger(__name__)

class SiteListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        developer = request.user
        if not hasattr(developer, 'company'):
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        show_archived = request.query_params.get('show_archived', 'false').lower() in ['true', '1']
        sites = Site.objects.filter(company=developer.company, archived=show_archived)
        serializer = SiteSerializer(sites, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new site for the developer's company.
        """
        developer = request.user
        logger.debug(f"Developer: {developer}, Company: {getattr(developer, 'company', None)}")

        if not hasattr(developer, 'company'):
            logger.error("Company not found for developer")
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Copy data to modify it
        data = request.data.copy()  # Make a mutable copy to avoid QueryDict issues
        data['company'] = developer.company.id
        logger.debug(f"Data before serialization: {data}")

        serializer = SiteSerializer(data=data)

        if serializer.is_valid():
            logger.debug("Serializer is valid. Saving the site.")
            serializer.save()
            logger.debug(f"Site created with ID: {serializer.data.get('id')}")
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        logger.error(f"Serializer validation failed. Errors: {serializer.errors}")
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SiteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve details of a specific site.
        """
        developer = request.user
        if not hasattr(developer, 'company'):
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=developer.company)
        serializer = SiteSerializer(site)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Update a site's details. Company cannot be updated.
        """
        developer = request.user
        if not hasattr(developer, 'company'):
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=developer.company)

        data = request.data.copy()  # Make a mutable copy to avoid QueryDict issues
        data.pop('company', None)  # Prevent editing the company field

        serializer = SiteSerializer(site, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Archive a site (soft delete).
        """
        developer = request.user
        if not hasattr(developer, 'company'):
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=developer.company)

        site.archived = True
        site.save()
        return Response({"success": True, "message": "Site archived successfully."}, status=status.HTTP_200_OK)

class StatusOptionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_options = dict(Site.STATUS_CHOICES) 
        return Response({"status_options": status_options}, status=200)