from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Milestone
from .serializers import MilestoneSerializer

class MilestoneListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: List milestones
    def get(self, request):
        milestones = Milestone.objects.all()
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data)

    # POST: Create a new milestone
    def post(self, request):
        serializer = MilestoneSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
          # Log the errors to debug
          print("Serializer errors:", serializer.errors)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilestoneDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Retrieve a specific milestone
    def get(self, request, pk):
        try:
            milestone = Milestone.objects.get(id=pk)
            serializer = MilestoneSerializer(milestone)
            return Response(serializer.data)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found"}, status=status.HTTP_404_NOT_FOUND)

    # PUT: Update an existing milestone
    def put(self, request, pk):
        try:
            milestone = Milestone.objects.get(id=pk)
            serializer = MilestoneSerializer(milestone, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found"}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: Delete a milestone
    def delete(self, request, pk):
        try:
            milestone = Milestone.objects.get(id=pk)
            milestone.delete()
            return Response({"message": "Milestone deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found"}, status=status.HTTP_404_NOT_FOUND)
