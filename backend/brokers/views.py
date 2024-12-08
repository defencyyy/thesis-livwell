from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from developers.models import Developer
from .models import Broker
from .serializers import DeveloperBrokerSerializer, EditBrokerSerializer


class BrokerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            brokers = Broker.objects.filter(company=company, archived=False)
            serializer = DeveloperBrokerSerializer(brokers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            data = request.data
            data['company'] = company.id

            serializer = DeveloperBrokerSerializer(data=data)

            if serializer.is_valid():
                broker = serializer.save()
                broker.username = f"{broker.id}.{broker.first_name}{broker.last_name}".lower()
                broker.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)


class BrokerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            broker = Broker.objects.get(id=pk, company=company)
            serializer = DeveloperBrokerSerializer(broker)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            broker = Broker.objects.get(id=pk, company=company)
            serializer = EditBrokerSerializer(broker, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            broker = Broker.objects.get(id=pk, company=company)

            # Archive the broker
            broker.archived = True
            broker.save()

            return Response({"message": "Broker archived successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)

class ArchivedBrokerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetch all archived brokers for the developer's company.
        """
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            archived_brokers = Broker.objects.filter(company=company, archived=True)
            serializer = DeveloperBrokerSerializer(archived_brokers, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """
        Unarchive a specific broker.
        """
        try:
            developer = Developer.objects.get(id=request.user.id)

            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            broker = Broker.objects.get(id=pk, company=company, archived=True)

            broker.archived = False
            broker.save()

            return Response({"message": "Broker unarchived successfully"}, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found or not archived"}, status=status.HTTP_404_NOT_FOUND)
