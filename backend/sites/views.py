from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from developers.models import Developer
from .models import Site
from .serializers import SiteSerializer

class SiteListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            developer = Developer.objects.get(id=request.user.id)
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            # Check if the query parameter 'show_archived' is true, else default to false
            show_archived = request.query_params.get('show_archived', 'false') == 'true'

            # If show_archived is true, include archived sites, else exclude them
            if show_archived:
                sites = Site.objects.filter(company=company)
            else:
                sites = Site.objects.filter(company=company, archived=False)

            serializer = SiteSerializer(sites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found."}, status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        try:
            developer = Developer.objects.get(id=request.user.id)
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            data = request.data.copy()
            data['company'] = company.id
            serializer = SiteSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found."}, status=status.HTTP_404_NOT_FOUND)

class SiteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            # Fetch site, considering the archived status based on the get request.
            site = Site.objects.get(pk=pk, company=company)
            serializer = SiteSerializer(site)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Site.DoesNotExist:
            return Response({"error": "Site not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            site = Site.objects.get(pk=pk, company=company)

            # Allow updating the 'archived' field if it's part of the request
            archived = request.data.get('archived', None)
            if archived is not None:
                site.archived = archived
                site.save()

            request.data.pop('company', None)  # Prevent editing the company field
            serializer = SiteSerializer(site, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Site.DoesNotExist:
            return Response({"error": "Site not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            site = Site.objects.get(pk=pk, company=company)

            # Toggle the archived status when the site is deleted (archived)
            site.archived = True
            site.save()
            return Response({"message": "Site archived successfully."}, status=status.HTTP_200_OK)
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Site.DoesNotExist:
            return Response({"error": "Site not found."}, status=status.HTTP_404_NOT_FOUND)
