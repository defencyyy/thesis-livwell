from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from .models import Developer
from brokers.models import Broker
from django.contrib.auth import authenticate

class DeveloperAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        developer = request.user
        return Response({
            "username": developer.username,
            "first_name": developer.first_name,
            "last_name": developer.last_name,
            "email": developer.email,
            "contact_number": developer.contact_number,
        })

    def put(self, request):
        user = request.user
        data = request.data

        # Validate current password
        current_password = data.get('current_password')
        if current_password and not check_password(current_password, user.password):
            return JsonResponse({"success": False, "message": "Incorrect current password."}, status=400)

        # Check if the new username is already taken by another developer
        new_username = data.get('username', user.username).lower()

        # Check if the username is taken by another developer
        if Developer.objects.filter(username=new_username).exclude(id=user.id).exists():
            return JsonResponse({"success": False, "message": "This username is already taken."}, status=400)

        # Check if the username is taken by a broker
        if Broker.objects.filter(username=new_username).exists():
            return JsonResponse({"success": False, "message": "This username is already taken."}, status=400)

        # Update fields
        user.username = new_username
        user.email = data.get('email', user.email)
        user.contact_number = data.get('contact_number', user.contact_number)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        # Handle password update (if provided)
        if data.get('new_password'):
            user.password = make_password(data['new_password'])

        # Save the updated user
        user.save()

        return JsonResponse({"success": True, "message": "Account updated successfully."})


class VerifyPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data.get("password")
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            return Response({"isValid": True})
        return Response({"isValid": False}, status=400)


