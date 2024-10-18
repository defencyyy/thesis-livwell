from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from brokers.models import Broker  # Import Broker from the Brokers app
from developers.models import Developer # Import Developer from the Developers app
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone  # Make sure to import timezone
from django.shortcuts import render
from django.conf import settings
import json
from django.contrib.auth.hashers import make_password


#For Brokers
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # Log the incoming request
            print("Received POST request for login.")

            # Parse the request body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"success": False, "message": "Username and password are required."}, status=400)

            # Find the broker by username
            broker = Broker.objects.get(username=username)

            # Check the password
            if not check_password(password, broker.password):
                return JsonResponse({"success": False, "message": "Invalid credentials."}, status=404)

            # Update the last login time
            broker.last_login = timezone.now()
            broker.save()

            return JsonResponse({"success": True, "message": "Login successful."}, status=200)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "User does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            # Log the error for debugging
            print(f"Error during login: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

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
            # Log the incoming request
            print("Received POST request to reset password.")

            data = json.loads(request.body)
            new_password = data.get('new_password')

            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            # Find the broker by uid
            broker = Broker.objects.get(pk=uid)

            # Check if the token is valid
            if not default_token_generator.check_token(broker, token):
                return JsonResponse({"success": False, "message": "Invalid or expired token."}, status=400)

            # Update the password
            broker.password = make_password(new_password)
            broker.save()

            return JsonResponse({"success": True, "message": "Password reset successfully!"}, status=200)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "Broker not found."}, status=404)
        except Exception as e:
            # Log the error for debugging
            print(f"Error resetting password: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

#For Developers
@csrf_exempt
def login_view_dev(request):
    if request.method == 'POST':
        try:
            print("Received POST request for developer login.")

            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"success": False, "message": "Username and password are required."}, status=400)

            # Assuming you have a Developer model like Broker
            developer = Developer.objects.get(username=username)  # Adjust for Developer

            if not check_password(password, developer.password):
                return JsonResponse({"success": False, "message": "Invalid credentials."}, status=404)

            developer.last_login = timezone.now()
            developer.save()

            return JsonResponse({"success": True, "message": "Login successful."}, status=200)

        except Developer.DoesNotExist:  # Adjust for Developer
            return JsonResponse({"success": False, "message": "Developer does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def send_dev_password_reset_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            developer = Developer.objects.get(email=email)

            # Generate a token
            token = default_token_generator.make_token(developer)

            # Create a password reset link for developers
            reset_link = reverse('DevResetPass', kwargs={'uid': developer.pk, 'token': token})

            # Assuming your Vue app is running on localhost:8080
            reset_link_full = f'http://localhost:8080/#/devresetpass/{developer.pk}/{token}/'

            # Send email
            send_mail(
                'Developer Password Reset',
                f'Click the link below to reset your password:\n{reset_link_full}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({"success": True, "message": "Password reset email sent"}, status=200)

        except Developer.DoesNotExist:
            return JsonResponse({"success": False, "message": "Developer not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": "An internal error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@csrf_exempt
def DevResetPass(request, uid, token):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_password = data.get('new_password')

            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            developer = Developer.objects.get(pk=uid)

            if not default_token_generator.check_token(developer, token):
                return JsonResponse({"success": False, "message": "Invalid or expired token."}, status=400)

            developer.password = make_password(new_password)
            developer.save()

            return JsonResponse({"success": True, "message": "Password reset successfully!"}, status=200)

        except Developer.DoesNotExist:
            return JsonResponse({"success": False, "message": "Developer not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
