from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Site
from .serializers import SiteSerializer

class SiteListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SiteDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            site = Site.objects.get(pk=pk)
            serializer = SiteSerializer(site)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            site = Site.objects.get(pk=pk)
            serializer = SiteSerializer(site, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            site = Site.objects.get(pk=pk)
            site.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Site.DoesNotExist:
            return Response({"error": "Site not found"}, status=status.HTTP_404_NOT_FOUND)
