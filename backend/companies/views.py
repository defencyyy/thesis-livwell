from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Company
from developers.models import Developer  # Import your custom Developer model
from .serializers import CompanySerializer

class CompanyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Adjust if request.user is not automatically mapped to a Developer instance
        try:
            developer = Developer.objects.get(email=request.user.email)  # Adjust if needed
            company = developer.company
        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=404)

        # Serialize the company data
        serializer = CompanySerializer(company)
        return Response(serializer.data)
