import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.db import transaction
from developers.models import Developer
from .models import Site, Section
from .serializers import SiteSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

# Set up logging
logger = logging.getLogger(__name__)

def get_developer_company(request):
    developer = request.user
    if not hasattr(developer, 'company'):
        return None
    return developer.company

def list_sections(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    sections = site.sections.all()
    return render(request, "sections/list.html", {"sections": sections, "site": site})

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
        sections_data = data.pop('sections', [])
        serializer = SiteSerializer(data=data)
        
        if serializer.is_valid():
            site = serializer.save()

            # Create the sections associated with the site
            for section_data in sections_data:
                Section.objects.create(site=site, **section_data)

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
        logging.debug("PUT request received for site ID: %s", pk)
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        site = get_object_or_404(Site, pk=pk, company=company)

        # Validate and update the site fields using the serializer
        serializer = SiteSerializer(site, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        archived_sites = Site.objects.filter(Q(company=company) & Q(archived=True))
        serializer = SiteSerializer(archived_sites, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        action = request.query_params.get("action")

        try:
            site = Site.objects.get(pk=pk, company=company)

            if action == "archive":
                site.archived = True
                site.save()
                return Response({"success": True, "message": "Site archived successfully."}, status=status.HTTP_200_OK)

            elif action == "unarchive":
                if not site.archived:
                    return Response(
                        {"error": "Site is not archived."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                site.archived = False
                site.save()
                return Response({"success": True, "message": "Site unarchived successfully."}, status=status.HTTP_200_OK)

            return Response(
                {"error": "Invalid action."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Site.DoesNotExist:
            return Response(
                {"error": "Site not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

class SiteWithFloorCountsView(APIView):
    def get(self, request, site_id):
        try:
            site = Site.objects.get(id=site_id)  # Get the site by ID
            section_data = site.sections_with_unit_counts()  # Call the method to get the floor data
            return Response({"success": True, "data": section_data}, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=status.HTTP_404_NOT_FOUND)

class SitePictureUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def put(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response(
                {"error": "Company not found for this developer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve the site
        try:
            site = Site.objects.get(id=pk, company=company)
        except Site.DoesNotExist:
            return Response(
                {"error": "Site not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the request contains a picture
        if 'picture' not in request.FILES:
            return Response(
                {"error": "No picture file uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the picture to the site
        picture = request.FILES['picture']
        site.picture = picture
        site.save()

        # Return the updated site data (including picture)
        serializer = SiteSerializer(site)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )
