from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from brokers.models import Broker  # Import Broker from the Brokers app
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone  # Make sure to import timezone
from django.shortcuts import render
from django.conf import settings
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
            broker = Broker.objects.get(email=email)

            # Generate a token
            token = default_token_generator.make_token(broker)

            # Create a password reset link (change this part)
            reset_link = reverse('BrokResetPass', kwargs={'uid': broker.pk, 'token': token})

            # Assuming your Vue app is running on localhost:8080
            reset_link_full = f'http://localhost:8080/#/brokresetpass/{broker.pk}/{token}/'

            # Send email
            send_mail(
                'Password Reset',
                f'Click the link below to reset your password:\n{reset_link_full}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": "Password reset email sent"}, status=200)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "Broker not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": "An internal error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

@csrf_exempt
def BrokResetPass(request, uid, token):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_password = data.get('new_password')

            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required"}, status=400)

            broker = get_object_or_404(Broker, pk=uid)

            # Check if the token is valid
            if default_token_generator.check_token(broker, token):
                broker.set_password(new_password)
                broker.save()
                return JsonResponse({"success": True, "message": "Password reset successfully"}, status=200)
            else:
                return JsonResponse({"success": False, "message": "Invalid token"}, status=400)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid user"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
