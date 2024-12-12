from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Milestone
from .serializers import MilestoneSerializer

# Assuming the get_developer_company function is defined like this:
def get_developer_company(request):
    developer = request.user
    if not hasattr(developer, 'company'):
        return None
    return developer.company

class MilestoneListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: List milestones for the developer's company
    def get(self, request):
        company = get_developer_company(request)
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)
        
        milestones = Milestone.objects.filter(company=company)  # Filter by company
        serializer = MilestoneSerializer(milestones, many=True)
        return Response(serializer.data)

    # POST: Create a new milestone for the developer's company
    def post(self, request):
        company = get_developer_company(request)
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)
        
        # Add the company to the request data before serializing
        data = request.data.copy()
        data['company'] = company.id
        
        serializer = MilestoneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Log the errors to debug
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MilestoneDetailView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Retrieve a specific milestone, only if it belongs to the developer's company
    def get(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            milestone = Milestone.objects.get(id=pk, company=company)  # Filter by company
            serializer = MilestoneSerializer(milestone)
            return Response(serializer.data)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found or does not belong to your company."}, status=status.HTTP_404_NOT_FOUND)

    # PUT: Update an existing milestone, only if it belongs to the developer's company
    def put(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            milestone = Milestone.objects.get(id=pk, company=company)  # Filter by company
            serializer = MilestoneSerializer(milestone, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found or does not belong to your company."}, status=status.HTTP_404_NOT_FOUND)

    # DELETE: Delete a milestone, only if it belongs to the developer's company
    def delete(self, request, pk):
        company = get_developer_company(request)
        if not company:
            return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            milestone = Milestone.objects.get(id=pk, company=company)  # Filter by company
            milestone.delete()
            return Response({"message": "Milestone deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Milestone.DoesNotExist:
            return Response({"error": "Milestone not found or does not belong to your company."}, status=status.HTTP_404_NOT_FOUND)
