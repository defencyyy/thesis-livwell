from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Developer
from .serializers import DeveloperSerializer  # Assuming you have a serializer for Developer

class DeveloperDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Authenticated User: {request.user}")  # Check user here
        if request.user.is_authenticated:
            developer = request.user
            serializer = DeveloperSerializer(developer)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not authenticated'}, status=403)
