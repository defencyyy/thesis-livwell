import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
from developers.models import Developer
from .models import Site, Floor
from .serializers import SiteSerializer

# Set up logging
logger = logging.getLogger(__name__)

def get_developer_company(request):
    developer = request.user
    if not hasattr(developer, 'company'):
        return None
    return developer.company

class SiteListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        show_archived = request.query_params.get('show_archived', 'false').lower() in ['true', '1']
        sites = Site.objects.filter(company=company, archived=show_archived)
        serializer = SiteSerializer(sites, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        company = get_developer_company(request)
        if not company:
            logger.error("Company not found for developer")
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Copy data to modify it
        data = request.data.copy()  # Make a mutable copy to avoid QueryDict issues
        data['company'] = company.id

        # Handle floors in the request
        floors_data = data.pop('floors', [])
        serializer = SiteSerializer(data=data)
        
        if serializer.is_valid():
            site = serializer.save()

            # Create the floors associated with the site
            for floor_data in floors_data:
                Floor.objects.create(site=site, **floor_data)

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

        logger.error(f"Serializer validation failed. Errors: {serializer.errors}")
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SiteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=company)
        serializer = SiteSerializer(site)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=company)

        data = request.data.copy()
        data['company'] = company.id

        # Extract floor data
        floors_data = data.pop('floors', [])

        # Serialize the site data
        serializer = SiteSerializer(site, data=data, partial=True)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Save site data
                    site = serializer.save()

                    # Process floors data: add or update floors
                    for floor_data in floors_data:
                        floor_number = floor_data.get('floor_number')

                        # Check if floor already exists
                        existing_floor = Floor.objects.filter(site=site, floor_number=floor_number).first()

                        if existing_floor:
                            # Update the existing floor
                            for field, value in floor_data.items():
                                setattr(existing_floor, field, value)
                            existing_floor.save()

                        else:
                            # Create a new floor if it doesn't exist
                            Floor.objects.create(site=site, **floor_data)

                    return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

            except Exception as e:
                logger.error(f"Error updating site and floors: {e}")
                return Response({"success": False, "error": "An error occurred while updating."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            logger.error(f"Serializer validation failed. Errors: {serializer.errors}")
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=company)

        site.archived = True
        site.save()
        return Response({"success": True, "message": "Site archived successfully."}, status=status.HTTP_200_OK)


class StatusOptionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_options = dict(Site.STATUS_CHOICES) 
        return Response({"status_options": status_options}, status=200)


class ArchivedSiteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all archived sites for the logged-in developer's company.
        """
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Use Q for more efficient querying
        archived_sites = Site.objects.filter(
            Q(company=company) & Q(archived=True)
        )
        serializer = SiteSerializer(archived_sites, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            site = Site.objects.get(pk=pk, company=company, archived=True)
            site.archived = False
            site.save()
            return Response({"success": True, "message": "Site unarchived successfully."}, status=status.HTTP_200_OK)
        
        except Site.DoesNotExist:
            return Response(
                {"error": "Site not found or not archived."},
                status=status.HTTP_404_NOT_FOUND,
            )


class SiteWithFloorCountsView(APIView):
    def get(self, request, site_id):
        try:
            site = Site.objects.get(id=site_id)  # Get the site by ID
            floor_data = site.floors_with_unit_counts()  # Call the method to get the floor data
            return Response({"success": True, "data": floor_data}, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=status.HTTP_404_NOT_FOUND)
