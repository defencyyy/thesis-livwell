from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Assuming the user has a foreign key to the Company model
        return Company.objects.filter(developer=self.request.user)

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only the company associated with the logged-in user
        return Company.objects.filter(developer=self.request.user)
