# Django Lib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils import timezone  
from django.db import models 
from django.utils.timezone import now  
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

from brokers.models import Broker 
from developers.models import Developer 
from customers.models import Customer
from sales.models import Sale
from units.models import Unit
from sites.models import Site

import json
import re

@csrf_exempt
def login_view(request, user_role):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse(
                    {"success": False, "message": "Username and password are required."},
                    status=400
                )

            # Fetch the user based on user_role
            if user_role == 'broker':
                user = Broker.objects.filter(username=username).first()
            elif user_role == 'developer':
                user = Developer.objects.filter(username=username).first()
            else:
                return JsonResponse({"success": False, "message": "Invalid user type."}, status=400)

            # Validate credentials
            if user is None or not check_password(password, user.password):
                return JsonResponse({"success": False, "message": "Invalid credentials."}, status=404)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Save last login timestamp
            user.last_login = now()
            user.save()

            # Return tokens and user data
            return JsonResponse({
                "success": True,
                "tokens": {
                    "access": access_token,
                    "refresh": str(refresh)
                },
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "contact_number": user.contact_number,
                    "user_role": user_role,
                    "company_id": user.company.id,  # Include the company ID here
                    "company_name": user.company.name,  # Include company name if needed
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def login_view_broker(request):
    return login_view(request, user_role='broker')

@csrf_exempt
def login_view_developer(request):
    return login_view(request, user_role='developer')

def validate_password_strength(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'\d', password):
        return "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None

@csrf_exempt
def refresh_token_view(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token:
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            response = JsonResponse({'success': True})
            response.set_cookie(
                'access_token', new_access_token, httponly=True, max_age=900
            )
            return response
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Refresh token not found'})

@csrf_exempt
def dev_logout_view(request):
    if request.method == 'POST':
        response = JsonResponse({'success': True})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

# Brokers
@csrf_exempt
def send_password_reset_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            broker = Broker.objects.get(email=email)

            token = default_token_generator.make_token(broker)

            reset_link = reverse('BrkResetPass', kwargs={'uid': broker.pk, 'token': token})

            reset_link_full = f'http://localhost:8080/#/broker/reset-pass/{broker.pk}/{token}/'

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

            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            password_error = validate_password_strength(new_password)
            if password_error:
                return JsonResponse({"success": False, "message": password_error}, status=400)

            broker = Broker.objects.get(pk=uid)

            if not default_token_generator.check_token(broker, token):
                return JsonResponse({"success": False, "message": "Invalid or expired token."}, status=400)

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

            if 'password' in data and data['password'] is not None:
                password = data['password']

                password_error = validate_password_strength(password)
                if password_error:
                    return JsonResponse({"success": False, "message": password_error}, status=400)

                broker.password = make_password(password)

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

            # Create a new customer instance, including company_id
            customer = Customer.objects.create(
                broker_id=data['broker'],
                company_id=data['company_id'],  # Include company_id
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

@csrf_exempt
def get_broker(request, broker_id):
    if request.method == 'GET':
        try:
            # Fetch the broker from the database
            broker = Broker.objects.get(id=broker_id)
            
            # Return the necessary details (including company_id)
            broker_data = {
                "id": broker.id,
                "company_id": broker.company_id,  # Adjust according to your field name
                "email": broker.email,
                # Add other fields you may need
            }
            return JsonResponse(broker_data, status=200)

        except Broker.DoesNotExist:
            return JsonResponse({"success": False, "message": "Broker not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def total_sales_view(request):
    if request.method == 'GET':
        broker_id = request.GET.get('broker_id')
        if not broker_id:
            return JsonResponse({'error': 'Broker ID not provided'}, status=400)

        # Calculate total sales with status "sold" for the given broker ID
        total_sales = Sale.objects.filter(broker_id=broker_id, status='sold').count()

        return JsonResponse({'total_sales': total_sales})

@csrf_exempt
def total_commissions_view(request):
    if request.method == 'GET':
        broker_id = request.GET.get('broker_id')
        if not broker_id:
            return JsonResponse({'error': 'Broker ID not provided'}, status=400)

        # Get all "sold" sales made by the broker
        sales = Sale.objects.filter(broker_id=broker_id, status='sold')
        
        # Extract unit IDs from the "sold" sales
        unit_ids = sales.values_list('unit_id', flat=True)

        # Sum up the commissions for these units
        total_commission = Unit.objects.filter(id__in=unit_ids).aggregate(total=models.Sum('commission'))['total'] or 0

        return JsonResponse({'total_commissions': total_commission})

@csrf_exempt
def site_sales_view(request):
    if request.method == 'GET':
        broker_id = request.GET.get('broker_id')
        if not broker_id:
            return JsonResponse({'error': 'Broker ID not provided'}, status=400)

        # Fetch sites and calculate total "sold" sales per site
        sites = []
        for site in Site.objects.all():  # Assuming you have a Site model
            total_sales = Sale.objects.filter(broker_id=broker_id, site_id=site.id, status='sold').count()
            sites.append({
                'id': site.id,
                'name': site.name,
                'picture': request.build_absolute_uri(site.picture.url) if site.picture else None,
                'total_sales': total_sales,
            })

        return JsonResponse({'sites': sites})
    
@csrf_exempt
def sales_details_view(request):
    if request.method == 'GET':
        site_id = request.GET.get('site_id')
        broker_id = request.GET.get('broker_id')

        if not site_id or not broker_id:
            return JsonResponse({'error': 'Site ID or Broker ID not provided'}, status=400)

        try:
            # Fetch "sold" sales related to the specified site and broker
            sales = Sale.objects.filter(
                unit__site_id=site_id,
                broker_id=broker_id,
                status='sold'
            ).select_related('unit', 'customer')

            sales_details = []
            for sale in sales:
                sales_details.append({
                    'unit_name': sale.unit.unit_title,
                    'customer_name': f"{sale.customer.first_name} {sale.customer.last_name}",
                    'date_sold': sale.date_sold.strftime("%Y-%m-%d")
                })

            return JsonResponse({'sales': sales_details})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def get_available_sites(request):
    if request.method == 'GET':
        # Fetch sites that are either 'preselling' or 'completed'
        sites = Site.objects.filter(status__in=['preselling', 'completed'])        
        # Prepare the response data
        site_data = []
        for site in sites:
            site_data.append({
                'id': site.id,
                'name': site.name,
                'description': site.description,
                'location': site.location,
                'picture': request.build_absolute_uri(site.picture.url) if site.picture else None,
            })
        
        return JsonResponse({'sites': site_data}, status=200)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_site_name(request, site_id):
    if request.method == 'GET':
        try:
            # Fetch the site based on the provided site_id
            site = Site.objects.get(id=site_id)
            created_year = site.created_at.year  # Extract the year from the created_at field
            return JsonResponse({
                'name': site.name,
                'created_year': created_year  # Return the creation year along with the site name
            }, status=200)

        except Site.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Site not found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
def get_available_units(request):
    if request.method == 'GET':
        site_id = request.GET.get('site_id')
        if not site_id:
            return JsonResponse({'success': False, 'message': 'Site ID not provided'}, status=400)

        try:
            # Fetch only units that are associated with the given site ID and have a status of 'available'
            units = Unit.objects.filter(site_id=site_id, status='available')

            # Prepare the response data
            unit_data = []
            for unit in units:
                unit_data.append({
                    'id': unit.id,
                    'unit_title': unit.unit_title,  # Adjust this to your actual field names
                    'picture':  request.build_absolute_uri(unit.picture.url) if unit.picture else None,
  # Include the picture URL (if available)
                    'price': unit.price,  # Include the price
                    'bedroom':unit.bedroom,
                    "bathroom":unit.bathroom,
                    "floor_area":unit.floor_area,
                    "floor":unit.floor,
                    "balcony":unit.balcony,
                    "view":unit.view,
                })

            return JsonResponse({'units': unit_data}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
def get_customers_for_broker(request, broker_id):
    try:
        # Fetch the broker
        broker = get_object_or_404(Broker, pk=broker_id)
        
        include_sales = request.GET.get('include_sales', 'false') == 'true'


        # Fetch customers for the broker
        customers = Customer.objects.filter(broker_id=broker_id)

        customer_data = []
        for customer in customers:
            # Basic customer info
            customer_name = f"{customer.first_name} {customer.last_name}"
            contact_number = customer.contact_number

            # If include_sales is True, fetch sales and related data
            if include_sales:
                sales = Sale.objects.filter(customer_id=customer.id)
                if sales.exists():
                    # For each sale, get the related site and unit
                    for sale in sales:
                        site = Site.objects.get(id=sale.site_id)
                        unit = Unit.objects.get(id=sale.unit_id)

                        customer_data.append({
                            'customer_name': customer_name,
                            'contact_number': contact_number,
                            'site': site.name,
                            'unit': unit.unit_title,
                            'document_status': "Pending",  # Adjust document status as needed
                        })
                else:
                    customer_data.append({
                        'customer_name': customer_name,
                        'contact_number': contact_number,
                        'site': "To be followed",
                        'unit': "To be followed",
                        'document_status': "Pending",
                    })
            else:
                # If no sales data, return just basic info (id and name)
                customer_data.append({
                    'id': customer.id,
                    'name': customer_name,
                })

        return JsonResponse({'success': True, 'customers': customer_data}, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

def fetch_sites(request):
    # Filter sites that have available units
    sites = Site.objects.filter(unit__status='available').distinct()

    site_data = []
    for site in sites:
        site_data.append({
            'id': site.id,
            'name': site.name,  # Site name
            'units': [
                {
                    'id': unit.id,
                    'unit_title': unit.unit_title  # Unit title
                }
                for unit in site.unit_set.filter(status='available')  # Only available units for the site
            ]
        })

    return JsonResponse({'sites': site_data}, safe=False)

# View to fetch units for a specific site
def fetch_units(request, site_id):
    # Fetch the site based on the ID
    site = get_object_or_404(Site, id=site_id)
    
    # Get available units for the site
    units = Unit.objects.filter(site=site, status='available')

    unit_data = [
        {
            'id': unit.id,
            'unit_title': unit.unit_title  # Return unit title
        }
        for unit in units
    ]

    return JsonResponse({'units': unit_data}, safe=False)


@csrf_exempt
def submit_sale(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            
            # Fetch related data from the database
            site = Site.objects.get(id=data['site'])

            unit = Unit.objects.get(id=data['unit'])

            broker = Broker.objects.get(id=data['broker'])

            company = broker.company

            # Fetch the customer based on the ID received in the request
            customer = Customer.objects.get(id=data['customer'])

            # Create a new sale record with the customer field populated
            sale = Sale.objects.create(
                customer=customer,  # Now pass the actual customer
                site=site,
                unit=unit,
                broker=broker,
                company=company,
                status='pending'  # Default status
            )
            print("Sale record created:", sale)

            # Update the unit status to 'pending' once the sale is made
            unit.status = 'pending'
            unit.save()

            # Return a success response
            return JsonResponse({'message': 'Sale submitted successfully!'}, status=201)

        except (Site.DoesNotExist, Unit.DoesNotExist, Broker.DoesNotExist, Customer.DoesNotExist) as e:
            return JsonResponse({'error': 'Invalid data or not found'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
@csrf_exempt
def fetch_sales(request):
    print("k")
    try:
        # Fetch all sales data with related customer, site, and unit using select_related for optimization
        sales_data = Sale.objects.all().select_related(
            'customer',  # Fetch customer details
            'site',      # Fetch site details
            'unit'       # Fetch unit details
        )

        # Prepare the response data
        sales = []
        for sale in sales_data:
            sales.append({
                'id': sale.id,
                'customer_name': f"{sale.customer.first_name} {sale.customer.last_name}",
                'site_name': sale.site.name,
                'unit_title': sale.unit.unit_title,
                'status': sale.status,
            })

        return JsonResponse({'sales': sales}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Developers
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

            password_error = validate_password_strength(new_password)
            if password_error:
                return JsonResponse({"success": False, "message": password_error}, status=400)

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
