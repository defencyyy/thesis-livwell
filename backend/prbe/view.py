from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from brokers.models import Broker  # Import Broker from the Brokers app
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone  # Make sure to import timezone
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"success": False, "message": "Missing username or password"}, status=400)

            try:
                broker = Broker.objects.get(username=username)
            except Broker.DoesNotExist:
                return JsonResponse({"success": False, "message": "User does not exist"}, status=404)

            if check_password(password, broker.password):
                broker.last_login = timezone.now()  # Update last_login to the current time
                broker.save()  # Save the updated broker object
                return JsonResponse({"success": True, "message": "Login successful"}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=400)

@csrf_exempt
def send_password_reset_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            print(f"Received email: {email}")  # Debug: print the received email

            # Check if the email is associated with any broker
            
            broker = Broker.objects.get(email=email)  # Check if email exists
            # If the broker is found, generate a token
            token = default_token_generator.make_token(broker)

            # Create a password reset link
            reset_link = request.build_absolute_uri(

            # Send email
            send_mail(
                'Password Reset',
                f'Click the link below to reset your password:\n{reset_link}',
                'noreply@example.com',
                [email],
                fail_silently= False,
            )
            return JsonResponse({"success": True, "message": "Password reset email sent"}, status=200)

        except Exception as e:
            print(f"An error occurred: {str(e)}")  # Print the error for debugging
            return JsonResponse({"success": False, "message": "An internal error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def reset_password_confirm(request, uid, token):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_password = data.get('new_password')
            broker = get_object_or_404(Broker, pk=uid)  # Retrieve broker instead of User

            # Check if the token is valid
            if default_token_generator.check_token(broker, token):
                broker.set_password(new_password)  # Use set_password for hashing
                broker.save()
                return JsonResponse({"success": True, "message": "Password reset successfully"}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Invalid token"}, status=400)

        except Broker.DoesNotExist:  # Change this to Broker
            return JsonResponse({"success": False, "message": "Invalid user"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
