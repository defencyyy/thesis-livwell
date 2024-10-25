# Django
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone  
from django.shortcuts import render
from django.conf import settings

# Non-Django
from brokers.models import Broker 
from developers.models import Developer 
from customers.models import Customer
from sales.models import Sale
import json
import re

@csrf_exempt
def login_view(request, user_type):
    if request.method == 'POST':
        try:
            print(f"Received POST request for {user_type} login.")

            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"success": False, "message": "Username and password are required."}, status=400)

            # Determine the model based on user_type
            if user_type == 'broker':
                user = Broker.objects.get(username=username)
            elif user_type == 'developer':
                user = Developer.objects.get(username=username)
            else:
                return JsonResponse({"success": False, "message": "Invalid user type."}, status=400)

            # Check the password
            if not check_password(password, user.password):
                return JsonResponse({"success": False, "message": "Invalid credentials."}, status=404)

            # Update the last login time
            user.last_login = timezone.now()
            user.save()

            return JsonResponse({
                "success": True,
                "user": {
                    "id": str(user.id),  # Include user ID
                    "username": user.username,
                    "email": user.email,
                    "contact_number": user.contact_number  # Ensure this field exists in your Broker model
                }
            }, status=200)

        except (Broker.DoesNotExist, Developer.DoesNotExist):
            return JsonResponse({"success": False, "message": "User does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def login_view_broker(request):
    return login_view(request, user_type='broker')

@csrf_exempt
def login_view_developer(request):
    return login_view(request, user_type='developer')

# For Brokers
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
            reset_link = reverse('BrkResetPass', kwargs={'uid': broker.pk, 'token': token})

            # Assuming your Vue app is running on localhost:8080
            reset_link_full = f'http://localhost:8080/#/broker/reset-pass/{broker.pk}/{token}/'

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
def BrkResetPass(request, uid, token):
    if request.method == 'POST':
        try:
            print("Received POST request to reset password.")
            data = json.loads(request.body)
            new_password = data.get('new_password')

            # Ensure password is provided
            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            # Password strength validation (same as in the account update)
            if len(new_password) < 8:
                return JsonResponse({"success": False, "message": "Password must be at least 8 characters long."}, status=400)
            if not re.search(r'[A-Z]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one uppercase letter."}, status=400)
            if not re.search(r'[a-z]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one lowercase letter."}, status=400)
            if not re.search(r'\d', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one number."}, status=400)
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one special character."}, status=400)

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
            print(f"Error resetting password: {e}")
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
@csrf_exempt
def update_broker_view(request, broker_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            broker = Broker.objects.get(id=broker_id)

            # Validate username uniqueness
            if 'username' in data and data['username'] is not None:
                if Broker.objects.filter(username=data['username']).exclude(id=broker_id).exists():
                    return JsonResponse({"success": False, "message": "Username already exists."}, status=400)
                broker.username = data['username']

            # Validate password strength
            if 'password' in data and data['password'] is not None:
                password = data['password']
                
                if len(password) < 8:
                    return JsonResponse({"success": False, "message": "Password must be at least 8 characters long."}, status=400)
                if not re.search(r"[A-Z]", password):
                    return JsonResponse({"success": False, "message": "Password must contain at least one uppercase letter."}, status=400)
                if not re.search(r"[a-z]", password):
                    return JsonResponse({"success": False, "message": "Password must contain at least one lowercase letter."}, status=400)
                if not re.search(r"\d", password):
                    return JsonResponse({"success": False, "message": "Password must contain at least one number."}, status=400)
                if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                    return JsonResponse({"success": False, "message": "Password must contain at least one special character."}, status=400)
                
                # Hash the password
                broker.password = make_password(password)

            # Update other fields
            if 'email' in data and data['email'] is not None:
                broker.email = data['email']
            if 'contact_number' in data and data['contact_number'] is not None:
                broker.contact_number = data['contact_number']

            broker.save()
            return JsonResponse({"success": True, "message": "Broker updated successfully."}, status=200)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "Broker does not exist."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error updating broker: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def add_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Create a new customer instance
            customer = Customer.objects.create(
                broker_id=data['broker'],
                email=data['email'],
                contact_number=data['contact_number'],
                affiliated_link=data.get('affiliated_link', ''),
                last_name=data['last_name'],
                first_name=data['first_name']
            )

            return JsonResponse({"success": True, "message": "Customer added successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def total_sales_view(request):
    if request.method == 'GET':
        broker_id = request.GET.get('broker_id')  # Get broker ID from the request
        if not broker_id:
            return JsonResponse({'error': 'Broker ID not provided'}, status=400)

        # Calculate total sales for the given broker ID
        total_sales = Sale.objects.filter(broker_id=broker_id).count()

        return JsonResponse({'total_sales': total_sales})

# For Developers
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
            reset_link_full = f'http://localhost:8080/#/developer/reset-pass/{developer.pk}/{token}/'

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

            # Ensure password is provided
            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            # Password strength validation
            if len(new_password) < 8:
                return JsonResponse({"success": False, "message": "Password must be at least 8 characters long."}, status=400)
            if not re.search(r'[A-Z]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one uppercase letter."}, status=400)
            if not re.search(r'[a-z]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one lowercase letter."}, status=400)
            if not re.search(r'\d', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one number."}, status=400)
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                return JsonResponse({"success": False, "message": "Password must contain at least one special character."}, status=400)

            # Find the developer by uid
            developer = Developer.objects.get(pk=uid)

            # Check if the token is valid
            if not default_token_generator.check_token(developer, token):
                return JsonResponse({"success": False, "message": "Invalid or expired token."}, status=400)

            # Update the password
            developer.password = make_password(new_password)
            developer.save()

            return JsonResponse({"success": True, "message": "Password reset successfully!"}, status=200)

        except Developer.DoesNotExist:
            return JsonResponse({"success": False, "message": "Developer not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)
