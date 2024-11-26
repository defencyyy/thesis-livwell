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
            # Get the developer associated with the logged-in user
            developer = Developer.objects.get(id=request.user.id)

            # Ensure the developer has an associated company
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company

            # Get brokers associated with the company
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

            # Create a new broker
            data = request.data
            data['company'] = company.id

            # Log the received data for debugging
            print("Received data for new broker:", data)

            serializer = DeveloperBrokerSerializer(data=data)

            if serializer.is_valid():
                try:
                    # Save the broker instance
                    broker = serializer.save()

                    # Generate username in the format `brokerid.fullname`
                    broker.username = f"{broker.id}.{broker.first_name}{broker.last_name}".lower()
                    broker.save()  # Save the updated username

                    # Return the serialized data after saving
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print("Error creating broker:", e)  # Log any error during save
                    return Response(
                        {"error": f"An error occurred: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            print("Validation errors:", serializer.errors)  # Log validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)


class BrokerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Get the developer associated with the logged-in user
            developer = Developer.objects.get(id=request.user.id)

            # Ensure the developer has an associated company
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            
            # Retrieve the broker only if they belong to the same company
            broker = Broker.objects.get(id=pk, company=company)
            serializer = DeveloperBrokerSerializer(broker)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Developer.DoesNotExist:
            return Response({"error": "Developer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            # Get the developer associated with the logged-in user
            developer = Developer.objects.get(id=request.user.id)

            # Ensure the developer has an associated company
            if not hasattr(developer, 'company'):
                return Response({"error": "Company not found for this developer."}, status=status.HTTP_404_NOT_FOUND)

            company = developer.company
            
            # Retrieve the broker only if they belong to the same company
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