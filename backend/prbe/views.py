# Django Lib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db import models 
from django.utils import timezone  
from django.utils.timezone import now  
from django.contrib.auth.hashers import check_password, make_password
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from django.db.models import Sum
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime
from django.core.cache import cache  # For caching tokens temporarily
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import random
import string




from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
SECRET_KEY = settings.SECRET_KEY


from developers.models import Developer
from brokers.models import Broker 
from customers.models import Customer
from sales.models import Sale
from units.models import Unit, UnitImage
from sites.models import Site
from documents.models import DocumentType, Document
from salesdetails.models import SalesDetails
from milestones.models import Milestone  
from companies.models import Company


from collections import Counter
import os
import json
import re
import logging

logger = logging.getLogger(__name__)

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
            if user_role == 'developer':
                user = Developer.objects.filter(username=username).first()
            elif user_role == 'broker':
                user = Broker.objects.filter(username=username).first()
            else:
                return JsonResponse({"success": False, "message": "Invalid user role."}, status=400)

            if user is None:
                return JsonResponse({"success": False, "message": "Invalid Credentials."}, status=404)

            if not check_password(password, user.password):
                return JsonResponse({"success": False, "message": "Invalid password."}, status=401)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Save last login timestamp
            user.last_login = now()
            user.save()

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
                    "company_id": user.company.id,
                }
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)
        except Exception as e:
            print(f"Error during login: {e}")
            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def login_view_developer(request):
    return login_view(request, user_role='developer')

@csrf_exempt
def login_view_broker(request):
    return login_view(request, user_role='broker')


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

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

@csrf_exempt
def brk_logout_view(request):
    if request.method == 'POST':
        response = JsonResponse({'success': True})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

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
# Function to generate a reset token
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return JsonResponse({"success": False, "message": "Username and email are required."}, status=400)

        # Check if the user exists in Broker or Developer models
        broker = Broker.objects.filter(username=username, email=email).first()
        developer = Developer.objects.filter(username=username, email=email).first()

        if not broker and not developer:
            return JsonResponse({"success": False, "message": "No account found with this username and email."}, status=404)

        user = broker if broker else developer

        # Generate a reset token
        reset_token = generate_reset_token()

        # Store the token in cache (valid for 1 hour)
        cache.set(f'password_reset_{reset_token}', user.id, timeout=3600)  # store user ID in the cache with the token

        # Send the reset email
        reset_link = f"http://localhost:8080/reset-password/{reset_token}/"  # Modify this URL to match your frontend
        send_mail(
            "Password Reset Request",
            f"Hello {user.username},\n\nPlease click the following link to reset your password: {reset_link}",
            'noreply@example.com',
            [email],
        )

        return JsonResponse({"success": True, "message": "Password reset instructions sent to your email."}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

@csrf_exempt
def reset_password(request, token):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_password = data.get('new_password')

            if not new_password:
                return JsonResponse({"success": False, "message": "New password is required."}, status=400)

            # Check if the token exists in cache and get the user ID
            user_id = cache.get(f'password_reset_{token}')

            if not user_id:
                return JsonResponse({"success": False, "message": "Invalid or expired token."}, status=400)

            # Retrieve the user associated with the token
            user = Broker.objects.filter(id=user_id).first() or Developer.objects.filter(id=user_id).first()

            if not user:
                return JsonResponse({"success": False, "message": "User not found."}, status=404)

            # Update the user's password
            user.password = make_password(new_password)
            user.save()

            # Optionally, delete the token from cache after using it
            cache.delete(f'password_reset_{token}')

            return JsonResponse({"success": True, "message": "Password reset successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)



@csrf_exempt
def get_broker_data(request, broker_id):
    try:
        # Fetch broker data from the database
        broker = Broker.objects.get(pk=broker_id)
        broker_data = {
            'username': broker.username,
            'email': broker.email,
            'contact_number': broker.contact_number,
        }
        return JsonResponse(broker_data, status=200)
    
    except Broker.DoesNotExist:
        return JsonResponse({'message': 'Broker not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@csrf_exempt
def update_broker_view(request, broker_id):
    print("l")
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            broker = Broker.objects.get(id=broker_id)

            # Get the company the broker belongs to
            company_id = broker.company.id  # Assuming the broker has a company ForeignKey
            current_password = data.get('current_password')
            
            if current_password and not broker.check_password(current_password):
                return JsonResponse({"success": False, "message": "Current password is incorrect."}, status=400)

            if 'password' in data and data['password'] is not None:
                password = data['password']
                password_error = validate_password_strength(password)
                if password_error:
                    return JsonResponse({"success": False, "message": password_error}, status=400)
                broker.password = make_password(password)

            if 'username' in data and data['username'] is not None:
                username = data['username']

                # Check if another broker in the same company has the same username
                if Broker.objects.filter(username=username, company_id=company_id).exclude(id=broker.id).exists():
                    return JsonResponse({"success": False, "message": "The username is already taken. Please choose a different one."}, status=400)

                # Check if a developer in the same company has the same username
                if Developer.objects.filter(username=username, company_id=company_id).exists():
                    return JsonResponse({"success": False, "message": "The username is already taken. Please choose a different one."}, status=400)

                broker.username = username
            
            if 'email' in data and data['email'] is not None:
                email = data['email']
                try:
                    validate_email(email)
                    if Broker.objects.filter(email=email).exclude(id=broker.id).exists():
                        return JsonResponse({"success": False, "message": "The email is already taken. Please choose a different one."}, status=400)
                    broker.email = email
                except ValidationError:
                    return JsonResponse({"success": False, "message": "Invalid email format."}, status=400)

            if 'contact_number' in data and data['contact_number'] is not None:
                contact_number = data['contact_number']
                # Add a validation for phone number format if needed
                if not re.match(r'^\+?[1-9]\d{1,14}$', contact_number):
                    return JsonResponse({"success": False, "message": "Invalid contact number format."}, status=400)
                broker.contact_number = contact_number

            broker.save()
            return JsonResponse({"success": True, "message": "Broker updated successfully."}, status=200)

        except Exception as e:
            error_message = str(e).lower()

            # Handle specific database errors like unique constraints
            if 'username' in error_message and 'already exists' in error_message:
                return JsonResponse({"success": False, "message": "The username is already staken. Please choose a different one."}, status=400)
            elif 'email' in error_message and 'already exists' in error_message:
                return JsonResponse({"success": False, "message": "The email is already taken. Please choose a different one."}, status=400)
            elif 'unique constraint' in error_message:
                return JsonResponse({"success": False, "message": "The provided data violates a unique constraint."}, status=400)

            return JsonResponse({"success": False, "message": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)


@csrf_exempt  # This decorator is optional if you are using CSRF tokens correctly in your request
def add_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            broker_id = data['broker']
            company_id = data['company_id']
            email = data['email']
            
            # Check if the email already exists for the same broker and company
            if Customer.objects.filter(email=email, broker_id=broker_id, company_id=company_id).exists():
                return JsonResponse({"success": False, "message": "Email already taken for this broker and company."}, status=400)

            # Create a new customer instance, including company_id
            customer = Customer.objects.create(
                broker_id=broker_id,
                company_id=company_id,  # Include company_id
                email=email,
                contact_number=data['contact_number'],
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
                "f_name":broker.first_name,
                "l_name":broker.last_name,
                "username":broker.username,
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
        total_sales = Sale.objects.filter(broker_id=broker_id, status='Sold').count()

        return JsonResponse({'total_sales': total_sales})

@csrf_exempt
def total_commissions_view(request):
    if request.method == 'GET':
        broker_id = request.GET.get('broker_id')
        if not broker_id:
            return JsonResponse({'error': 'Broker ID not provided'}, status=400)

        # Get all "sold" sales made by the broker
        sales = Sale.objects.filter(broker_id=broker_id, status='Sold')
        
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
            total_sales = Sale.objects.filter(broker_id=broker_id, site_id=site.id, status='Sold').count()
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
                status='Sold'
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
        company_id = request.GET.get('company_id')

        if not company_id:
            logger.error("Company ID not provided in the request.")
            return JsonResponse({'success': False, 'message': 'Company ID is required.'}, status=400)

        try:
            logger.debug(f"Fetching sites for company_id: {company_id}")
            sites = Site.objects.filter(company_id=company_id, status__in=['preselling', 'completed'])
            logger.debug(f"Found {sites.count()} sites for company_id: {company_id}")

            site_data = []
            for site in sites:
                available_units = Unit.objects.filter(site=site, status='Available')
                logger.debug(f"Site ID: {site.id}, Name: {site.name}, Available Units: {available_units.count()}")
                if available_units.exists():
                    site_data.append({
                        'id': site.id,
                        'name': site.name,
                        'description': site.description,
                        'location': site.location,
                        'picture': request.build_absolute_uri(site.picture.url) if site.picture else None,
                        'status':site.status,
                    })
            logger.info(f"Returning {len(site_data)} sites with available units.")
            return JsonResponse({'sites': site_data}, status=200)

        except Exception as e:
            logger.error(f"Error fetching sites: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    logger.error("Invalid request method.")
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
        logger.debug("Received request to fetch available units for site ID: %s", site_id)
        
        if not site_id:
            logger.error("Site ID not provided in the request.")
            return JsonResponse({'success': False, 'message': 'Site ID not provided'}, status=400)

        try:
            # Fetch only units that are associated with the given site ID and have a status of 'available'
            units = Unit.objects.filter(site_id=site_id, status='Available')
            logger.debug("Found %d available units for site ID %s", units.count(), site_id)

            # Prepare the response data
            unit_data = []
            for unit in units:
                images = UnitImage.objects.filter(unit_id=unit.id, image_type='unit')
                image_urls = [request.build_absolute_uri(image.image.url) for image in images]

                # Get the unit type name (you can also include more fields as needed)
                unit_type_name = unit.unit_type.name if unit.unit_type else None

                unit_info = {
                    'id': unit.id,
                    'months':unit.site.maximum_months,
                    'unit_title': unit.unit_title,
                    'images': image_urls,
                    'price': unit.price,
                    'bedroom': unit.bedroom,
                    'bathroom': unit.bathroom,
                    'floor_area': unit.floor_area,
                    'section': unit.section.number,
                    'balcony': unit.balcony,
                    'type': unit_type_name,  # Add the unit type here
                    'view': unit.view,
                    'company_id': unit.company.id,
                    'unit_number': unit.unit_number,
                    'lot_area': unit.lot_area,
                    'reservation_fee': unit.reservation_fee,
                    'other_charges': unit.other_charges,
                    'TLP_Discount': unit.spot_discount_flat,
                    'spot_discount': unit.spot_discount_percentage,
                    'vat_percent': unit.vat_percentage,
                    'commission':unit.commission,
                }
                logger.debug("Processed unit data: %s", unit_info)
                unit_data.append(unit_info)

            return JsonResponse({'units': unit_data}, status=200)

        except Exception as e:
            logger.error("Error while fetching units for site ID %s: %s", site_id, str(e))
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    logger.warning("Invalid request method: %s", request.method)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
@csrf_exempt
def get_unit_details(request, unit_id):
    if request.method == 'GET':
        logger.debug("Received request to fetch details for unit ID: %s", unit_id)

        try:
            # Fetch the unit with the given unit ID
            unit = Unit.objects.select_related('site', 'unit_type', 'section').get(id=unit_id)

            # Fetch unit images
            images = UnitImage.objects.filter(unit_id=unit.id, image_type='unit')
            image_urls = [request.build_absolute_uri(image.image.url) for image in images]

            # Prepare unit details
            unit_details = {
                'id': unit.id,
                'months': unit.site.maximum_months,
                'unit_title': unit.unit_title,
                'images': image_urls,
                'price': unit.price,
                'bedroom': unit.bedroom,
                'bathroom': unit.bathroom,
                'floor_area': unit.floor_area,
                'section': unit.section.number if unit.section else None,
                'balcony': unit.balcony,
                'type': unit.unit_type.name if unit.unit_type else None,
                'view': unit.view,
                'company_id': unit.company.id,
                'unit_number': unit.unit_number,
                'lot_area': unit.lot_area,
                'reservation_fee': unit.reservation_fee,
                'other_charges': unit.other_charges,
                'TLP_Discount': unit.spot_discount_flat,
                'spot_discount': unit.spot_discount_percentage,
                'vat_percent': unit.vat_percentage,
                'commission': unit.commission,
                'site': {
                    'id': unit.site.id,
                    'name': unit.site.name,
                    'months': unit.site.maximum_months,
                },
            }
            logger.debug("Fetched unit details: %s", unit_details)

            return JsonResponse({'success': True, 'unit': unit_details}, status=200)

        except Unit.DoesNotExist:
            logger.error("Unit with ID %s does not exist.", unit_id)
            return JsonResponse({'success': False, 'message': 'Unit not found'}, status=404)

        except Exception as e:
            logger.error("Error fetching unit details for ID %s: %s", unit_id, str(e))
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    logger.warning("Invalid request method: %s", request.method)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
def get_customers_for_broker(request, broker_id):
    try:
        # Fetch the broker
        broker = get_object_or_404(Broker, pk=broker_id)
        
        include_sales = request.GET.get('include_sales', 'false') == 'true'
        

                # Fetch customers for the broker
        customers = Customer.objects.filter(broker_id=broker_id, archived=False)
        total_customers = customers.count()

        customer_data = []
        required_document_types = DocumentType.objects.all()

        for customer in customers:
            customer_name = f"{customer.first_name} {customer.last_name}"
            contact_number = customer.contact_number
            company_id = customer.company.id
            document_status = "Pending"

            
            if include_sales:
                sales = Sale.objects.filter(customer_id=customer.id)
                
                if sales.exists():
                    for sale in sales:
                        site = Site.objects.get(id=sale.site_id)
                        unit = Unit.objects.get(id=sale.unit_id)
                        submitted_documents = Document.objects.filter(customer=customer, sales_id=sale.id)
                        submitted_document_types = {doc.document_type.id for doc in submitted_documents}
                        
                        all_documents_submitted = all(
                            req_doc.id in submitted_document_types for req_doc in required_document_types
                        )
                        document_status = "Complete" if all_documents_submitted else "Pending"

                        customer_entry = {
                            'id': customer.id,
                            'customer_name': customer_name,
                            'customer_code': customer.customer_code,
                            'f_name': customer.first_name,
                            'l_name': customer.last_name,
                            'contact_number': contact_number,
                            'email': customer.email,
                            'site': site.name,
                            'status': sale.status,
                            'unit': unit.unit_title,
                            'sales_id': sale.id,
                            'company_id': company_id,
                            'document_status': document_status,
                        }
                        customer_data.append(customer_entry)
                else:
                    customer_entry = {
                        'id': customer.id,
                        'customer_name': customer_name,
                        'customer_code': customer.customer_code,
                        'contact_number': contact_number,
                        'f_name': customer.first_name,
                        'l_name': customer.last_name,
                        'email': customer.email,
                        'sales_id': None,
                        'site': "To be followed",
                        'unit': "To be followed",
                        'status': "No sale",  # Fixed undefined 'sale'
                        'company_id': company_id,
                        'document_status': "Pending",
                    }
                    customer_data.append(customer_entry)
            else:
                customer_entry = {
                    'id': customer.id,
                    'customer_name': customer_name,
                    'name': customer_name,
                    'customer_code': customer.customer_code,
                    'f_name': customer.first_name,
                    'l_name': customer.last_name,
                    'email': customer.email,
                    'contact_number': contact_number,
                    'status': "No sales info",
                    'company_id': company_id,
                }
                customer_data.append(customer_entry)

        return JsonResponse({
            'success': True,
            'total_customers': total_customers,
            'customers': customer_data
        }, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def update_customer(request, customer_id):
    """
    Update customer details such as email, contact_number, first_name, and last_name.
    """
    if request.method == "PUT":
        try:
            # Get customer object by ID or return 404 if not found
            customer = get_object_or_404(Customer, id=customer_id)

            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Extract customer details from the request data
            email = data.get("email")
            contact_number = data.get("contact_number")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            # Validate the input data (you can add more validation as per your needs)
            if not email or not contact_number or not first_name or not last_name:
                return JsonResponse({"success": False, "message": "All fields are required."}, status=400)

            # Update the customer data
            customer.email = email
            customer.contact_number = contact_number
            customer.first_name = first_name
            customer.last_name = last_name

            # Save the updated customer object to the database
            customer.save()

            # Return a success response
            return JsonResponse({"success": True, "message": "Customer updated successfully!"})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    else:
        # Return a 405 Method Not Allowed if it's not a PUT request
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)

def fetch_sites(request):
    # Filter sites that have available units
    sites = Site.objects.filter(unit__status='Available').distinct()

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
                for unit in site.unit_set.filter(status='Available')  # Only available units for the site
            ]
        })

    return JsonResponse({'sites': site_data}, safe=False)

# View to fetch units for a specific site
def fetch_units(request, site_id):
    # Fetch the site based on the ID
    site = get_object_or_404(Site, id=site_id)
    
    # Get available units for the site
    units = Unit.objects.filter(site=site, status='Available')

    unit_data = [
        {
            'id': unit.id,
            'unit_title': unit.unit_title  # Return unit title
        }
        for unit in units
    ]

    return JsonResponse({'units': unit_data}, safe=False)

def fetch_sales(request):
    try:
        broker_id = request.GET.get('broker_id')

        # Fetch sales based on the broker_id, if provided
        if broker_id:
            sales = Sale.objects.filter(broker__id=broker_id,is_archived=False).select_related(
                'customer',  # Fetch related customer data
                'site',      # Fetch related site data
                'unit',      # Fetch related unit data
                'broker'     # Fetch related broker data
            )
        else:
            # If no broker_id is provided, return all sales (optional)
            sales = Sale.objects.all().select_related(
                'customer', 'site', 'unit', 'broker'
            )

        sales_data = []
        for sale in sales: 
            # Add sale data to the list, including full names and titles
            sales_data.append({
                'sale_id': sale.id,  # Include the sale ID
                'customer_name': f"{sale.customer.first_name} {sale.customer.last_name}",
                'customer_id': sale.customer.id,   # customer_id
                'customer_code':sale.customer.customer_code,
                'site_name': sale.site.name,
                'site_id': sale.site.id,           # site_id
                'unit_title': sale.unit.unit_title,
                'unit_id': sale.unit.id,           # unit_id
                'price': sale.unit.price,
                'status': sale.status,
                'email': sale.customer.email,
                'broker_id': sale.broker.id if sale.broker else None, # broker_id
                'broker_name': f"{sale.broker.first_name} {sale.broker.last_name}" if sale.broker else None,  # broker_name  
                'reservation_fee': sale.unit.reservation_fee,  # If reservation fee is required
                'other_charges': sale.unit.other_charges,  # Any other charges
                'TLP_Discount':sale.unit.spot_discount_flat,
                'spot_discount':sale.unit.spot_discount_percentage,
                'vat_percent':sale.unit.vat_percentage,  
                'months':sale.site.maximum_months, 
            })      
         # Group the sales by status and count occurrences
        status_count = Counter(sale.status for sale in sales)

        # Prepare the data to send to the frontend
        sales_status_data = {
            'sold': status_count.get('Sold', 0),
            'pending': status_count.get('Pending Reservation', 0),
            'reserved': status_count.get('Reserved', 0),
            'Pending_sold': status_count.get('Pending Sold', 0),
        }

        return JsonResponse({'success': True, 'sales': sales_data, 'sales_status_data': sales_status_data}, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@csrf_exempt
def reserve_unit(request):
    print("submitting reservation")
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request data
            data = json.loads(request.body)

            # Ensure the IDs are integers (if they are not already)
            customer_id = data.get('customer_name')
            site_id = int(data.get('site_id'))  # Convert to integer
            unit_id = int(data.get('unit_id'))  # Convert to integer
            broker_id = int(data.get('broker_id'))  # Convert to integer
            company_id = int(data.get('company_id'))  # Ensure company_id is an integer
            payment_amount = data.get('payment_amount')
            payment_method = data.get('payment_method')
            payment_reference = data.get('payment_reference')
            reservation_file = data.get('reservation_file')  # Just the filename in this case
            commission=data.get('commission')

            # Fetch the related objects from the database
            customer = Customer.objects.get(id=customer_id)
            site = Site.objects.get(id=site_id)
            unit = Unit.objects.get(id=unit_id)
            broker = Broker.objects.get(id=broker_id)

            # Create the Sale object
            sale = Sale.objects.create(
                customer=customer,
                site=site,
                unit=unit,
                broker=broker,
                company_id=company_id,
                status='Pending Reservation',  # Set to pending reservation
                reservation_fee=payment_amount,
                payment_method=payment_method,
                payment_reference=payment_reference,
                reservation_file=reservation_file if reservation_file else None,
                commission=commission
            )
            # Update the unit status to pending_reservation
            unit.status = 'Pending Reservation'
            unit.save()

            # Return a success response
            return JsonResponse({'message': 'Sale created successfully', 'sale_id': sale.id}, status=201)

        except Exception as e:
            # If something goes wrong, return an error response
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def submit_sales(request):
    if request.method == 'POST':
        try:
            # Get form data (request.POST) and file data (request.FILES)
            customer_id = request.POST.get('customer_id')
            site_id = request.POST.get('site_id')
            unit_id = request.POST.get('unit_id')
            sales_id=request.POST.get('sales_id')
            broker_id = request.POST.get('broker_id')
            payment_plan = request.POST.get('payment_plan')
            spot_discount_percent = request.POST.get('spot_discount_percent')
            tlp_discount_percent = request.POST.get('tlp_discount_percent')
            other_charges_percent = request.POST.get('other_charges_percent')
            spot_downpayment_percent = request.POST.get('spot_downpayment_percent')
            reservation_fee = request.POST.get('reservation_fee')
            spread_downpayment_percent = request.POST.get('spread_downpayment_percent')
            payable_months = request.POST.get('payable_months')
            payable_per_month = request.POST.get('payable_per_month')
            balance_upon_turnover = request.POST.get('balance_upon_turnover')
            net_unit_price = request.POST.get('net_unit_price')
            total_amount_payable = request.POST.get('total_amount_payable')
            net_full_payment = request.POST.get('net_full_payment')
            customer_email = request.POST.get('customer_email')

            # Get the uploaded file
            reservation_agreement = request.FILES.get('reservation_agreement')

            if reservation_agreement:
                # Save the file to the server (this is optional, depending on your requirement)
                file_path = default_storage.save(f'reservations/{reservation_agreement.name}', reservation_agreement)
            else:
                file_path = None
                        

            # Create a new SalesDetails entry
            sales_detail = SalesDetails.objects.create(
                customer_id=customer_id,
                site_id=site_id,
                unit_id=unit_id,
                broker_id=broker_id,
                sales_id=sales_id,
                payment_plan=payment_plan,
                spot_discount_percent=spot_discount_percent,
                tlp_discount_percent=tlp_discount_percent,
                other_charges_percent=other_charges_percent,
                spot_downpayment_percent=spot_downpayment_percent,
                reservation_fee=reservation_fee,
                spread_downpayment_percent=spread_downpayment_percent,
                payable_months=payable_months,
                payable_per_month=payable_per_month,
                balance_upon_turnover=balance_upon_turnover,
                net_unit_price=net_unit_price,
                total_amount_payable=total_amount_payable,
                net_full_payment=net_full_payment,
                reservation_agreement=file_path,  # Save the file path or reference in the model
            )

            # Optionally, send a confirmation email to the customer
            send_confirmation_email(request, customer_email, sales_detail)

            return JsonResponse({'success': True, 'message': 'Sales agreement submitted successfully.'}, status=200)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid method.'}, status=405)


def get_sales_detail(request, sales_detail_id):
    # Fetch the sales detail by UUID instead of ID
    sales_detail = get_object_or_404(SalesDetails, uuid=sales_detail_id)

    # Fetch the related site, broker, customer, and unit
    site = get_object_or_404(Site, id=sales_detail.site_id)
    broker = get_object_or_404(Broker, id=sales_detail.broker_id)
    customer = get_object_or_404(Customer, id=sales_detail.customer_id)
    unit = get_object_or_404(Unit, id=sales_detail.unit_id)
    company = get_object_or_404(Company, id=broker.company_id)

    # Prepare the response data with all related information
    sales_detail_data = {
        'uuid': sales_detail_id,  # Use uuid here instead of id
        'id':sales_detail.id,
        'customer_id': sales_detail.customer_id,
        'sales_id':sales_detail.sales_id,
        'site_id': sales_detail.site_id,
        'unit_id': sales_detail.unit_id,
        'broker_id': sales_detail.broker_id,
        'payment_plan': sales_detail.payment_plan,
        'spot_discount_percent': sales_detail.spot_discount_percent,
        'tlp_discount_percent': sales_detail.tlp_discount_percent,
        'other_charges_percent': sales_detail.other_charges_percent,
        'spot_downpayment_percent': sales_detail.spot_downpayment_percent,
        'reservation_fee': sales_detail.reservation_fee,
        'spread_downpayment_percent': sales_detail.spread_downpayment_percent,
        'payable_months': sales_detail.payable_months,
        'payable_per_month': sales_detail.payable_per_month,
        'balance_upon_turnover': sales_detail.balance_upon_turnover,
        'net_unit_price': sales_detail.net_unit_price,
        'total_amount_payable': sales_detail.total_amount_payable,
        'net_full_payment': sales_detail.net_full_payment,

        # Add related data
        'unit_price': unit.price,
        'site_name': site.name,  # Site name
        'broker_name': f"{broker.first_name} {broker.last_name}",  # Broker full name
        'customer_name': f"{customer.first_name} {customer.last_name}",  # Customer full name
        'unit_name': unit.unit_title, # Unit title
        'company_name': company.name,  # Company name

    }

    # Add the reservation agreement URL
    if sales_detail.reservation_agreement:
        base_url = 'http://localhost:8000'  # This is your domain or base URL
        reservation_agreement_url = base_url + settings.MEDIA_URL + str(sales_detail.reservation_agreement)

        # Add the URL to the response data
        sales_detail_data['reservation_agreement_url'] = reservation_agreement_url
    else:
        sales_detail_data['reservation_agreement_url'] = None

    # Return the response with the reservation agreement URL
    return JsonResponse(sales_detail_data)

def download_reservation_agreement(request, sales_detail_id):
    # Fetch the sales detail
    sales_detail = get_object_or_404(SalesDetails, id=sales_detail_id)

    # Check if the reservation agreement exists
    if sales_detail.reservation_agreement:
        # Get the path to the file
        file_path = os.path.join(settings.MEDIA_ROOT, str(sales_detail.reservation_agreement))

        # Ensure the file exists
        if os.path.exists(file_path):
            # Open the file and return it as a FileResponse with download headers
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            return response
        else:
            raise Http404("File not found.")
    else:
        raise Http404("Reservation agreement not available.")


def send_confirmation_email(request, customer_email, sales_detail):
    frontend_base_url = 'http://localhost:8080'  # Or use settings if you'd prefer dynamic configuration
    
    # Generate the URL to view the sales details on the frontend using the UUID
    sales_detail_url = f"{frontend_base_url}/sales-details/{sales_detail.uuid}/"

    # Compose the email content
    subject = 'Your Sales Agreement Details'
    message = f"Dear Customer,\n\nThank you for your purchase! You can view the details of your sales agreement using the link below:\n{sales_detail_url}\n\nBest regards,\nThe Sales Team"
    from_email = settings.DEFAULT_FROM_EMAIL  # Make sure to configure this in settings.py

    # Send the email
    send_mail(subject, message, from_email, [customer_email])


def check_sales_details(request, customer_id, site_id, unit_id):
    # Check if sales details exist for the given customer, site, and unit
    try:
        sales_details = SalesDetails.objects.get(
            customer_id=customer_id, 
            site_id=site_id, 
            unit_id=unit_id
        )
        
        # If sales details are found, return them in the response
        response_data = {
            'exists': True,
            'details': {
                'payment_plan': sales_details.payment_plan,
                'spot_discount': sales_details.spot_discount_percent,
                'tlp_discount': sales_details.tlp_discount_percent,
                'net_unit_price': sales_details.net_unit_price,
                'total_amount_payable': sales_details.total_amount_payable,
                'downpayment': sales_details.spot_downpayment_percent,
                'reservation_fee': sales_details.reservation_fee,
                'spread_downpayment_percent': sales_details.spread_downpayment_percent,
                'spot_downpayment_percent':sales_details.spot_downpayment_percent,
                'payable_months': sales_details.payable_months,
                'payable_per_month': sales_details.payable_per_month,
                'balance_upon_turnover': sales_details.balance_upon_turnover,
                'net_unit_price': sales_details.net_unit_price,
                'total_amount_payable': sales_details.total_amount_payable,
                'net_full_payment': sales_details.net_full_payment,
                'other_charges_percent': sales_details.other_charges_percent,
                'unit_price':sales_details.unit.price,

            }
        }
    except SalesDetails.DoesNotExist:
        # If no sales details are found, return exists=False
        response_data = {'exists': False}

    return JsonResponse(response_data)

def fetch_document_types(request):
    try:
        # Get the company ID from the request (query parameter or user's session)
        company_id = request.GET.get("company_id")

        # Ensure company_id is provided and valid
        if not company_id:
            return JsonResponse({"success": False, "message": "Company ID is required"}, status=400)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid Company ID"}, status=404)

        # Filter document types by company
        document_types = DocumentType.objects.filter(company=company)

        # Prepare the response data
        document_types_data = [
            {"id": dt.id, "name": dt.name, "description": dt.description}
            for dt in document_types
        ]

        return JsonResponse({"success": True, "documentTypes": document_types_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@csrf_exempt
def upload_document(request):
    if request.method == "POST":
        # Get the data from the request
        customer_id = request.POST.get("customer")
        company_id = request.POST.get("company")
        sales_id = request.POST.get("sales_id")

        files = request.FILES.getlist("files[]")
        document_type_ids = request.POST.getlist("document_types[]")

        if not customer_id or not document_type_ids or not files or not sales_id:
            return JsonResponse({"success": False, "message": "Missing required fields."}, status=400)

        try:
            # Fetch the customer object
            customer = get_object_or_404(Customer, id=customer_id)

            # Ensure each file is explicitly mapped to a document type
            if len(files) != len(document_type_ids):
                print(f"Error: Mismatch between number of files and document types. Files: {len(files)}, Document Types: {len(document_type_ids)}")
                return JsonResponse({"success": False, "message": "Mismatch between files and document types."}, status=400)

            # Debug: Print each file with its document type
            for i, file in enumerate(files):
                document_type_id = document_type_ids[i]

                document_type = get_object_or_404(DocumentType, id=document_type_id)

                # Check if a document already exists for this customer, document type, and sales_id
                existing_document = Document.objects.filter(
                    customer_id=customer_id,
                    document_type=document_type,
                    sales_id=sales_id
                ).first()

                if existing_document:
                    # If the document already exists, update it with the new file
                    existing_document.file = file
                    existing_document.save()
                else:
                    # If the document doesn't exist, create a new document for the specific sale
                    Document.objects.create(
                        customer_id=customer_id,
                        document_type=document_type,
                        company_id=company_id,
                        sales_id=sales_id,  # Associate the document with the specific sale
                        file=file,
                    )

            return JsonResponse({"success": True, "message": "Documents uploaded successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)




# Fetch documents for a given customer and sale
@csrf_exempt
def fetch_customer_documents(request, customer_id, sales_id):
    try:
        # Get the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Fetch documents for the customer and specific sale
        documents = Document.objects.filter(customer=customer, sales_id=sales_id)

        # Log the fetched documents

        # Prepare a list to return
        document_data = []
        for doc in documents:
            doc_info = {
                'id': doc.id,
                'document_type_id': doc.document_type.id,
                'document_type_name': doc.document_type.name,
                'file_name': os.path.basename(doc.file.name),
                'uploaded_at': doc.uploaded_at.isoformat(),
            }
            document_data.append(doc_info)

        # Return JSON response
        return JsonResponse({
            'success': True,
            'documents': document_data,
        })

    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Customer not found.'
        }, status=404)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print the error
        return JsonResponse({
            'success': False,
            'message': str(e),
        }, status=500)


@csrf_exempt
def mark_unit_as_sold(request, customer_id, sales_id):
    try:
        # Get the customer and sales instance
        customer = Customer.objects.get(id=customer_id)
        sale = Sale.objects.get(id=sales_id)

        # Assuming 'sale.company' provides the company related to the sale
        company = sale.company

        # Fetch the required document types for the specific company
        required_document_types = DocumentType.objects.filter(company=company)

        # Fetch the documents the customer has submitted for this sale
        submitted_documents = Document.objects.filter(customer=customer, sales_id=sales_id)
        submitted_document_types = {doc.document_type.id for doc in submitted_documents}

        
        # Check if the customer has submitted all required documents
        all_documents_submitted = all(
            req_doc.id in submitted_document_types for req_doc in required_document_types
        )

        # If all documents are submitted, mark the unit as sold
        if all_documents_submitted:
            sale.status = 'Pending Sold'  # Assuming 'sold' is a valid status for the sale
            sale.save()

            return JsonResponse({
                'success': True,
                'message': 'Unit successfully marked as sold.',
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'The customer has not submitted all required documents.',
            })

    except Customer.DoesNotExist:
        print("Customer not found with ID:", customer_id)
        return JsonResponse({
            'success': False,
            'message': 'Customer not found.'
        }, status=404)

    except Sale.DoesNotExist:
        print("Sale not found with ID:", sales_id)
        return JsonResponse({
            'success': False,
            'message': 'Sale not found.'
        }, status=404)

    except Exception as e:
        print("Error:", str(e))  # Log the exception
        return JsonResponse({
            'success': False,
            'message': str(e),
        }, status=500) 
   
def get_milestones(request):
    try:
        broker_id = request.GET.get('broker_id')  # Get broker_id from query parameter
        broker = Broker.objects.get(id=broker_id)  # Retrieve broker by id
        milestones = Milestone.objects.filter(company=broker.company)

        # Calculate total sales and commission
        total_sales = Sale.objects.filter(broker_id=broker_id, status='Sold').count()
        sales = Sale.objects.filter(broker_id=broker_id, status='Sold')

        # Extract unit IDs from the "sold" sales (if any sales exist)
        if sales.exists():
            unit_ids = sales.values_list('unit_id', flat=True)
            total_commission = Unit.objects.filter(id__in=unit_ids).aggregate(total=models.Sum('commission'))['total'] or 0
        else:
            total_commission = 0  # No sales, so commission is 0
        
        # Separate achieved and next milestones
        achieved_milestones = []
        next_milestones = []

        for milestone in milestones:
            if milestone.type == 'sales' and total_sales >= milestone.sales_threshold:
                achieved_milestones.append(milestone)
            elif milestone.type == 'commission' and total_commission >= milestone.commission_threshold:
                achieved_milestones.append(milestone)
            else:
                next_milestones.append(milestone)

        # Prepare data for response
        data = {
            'achieved_milestones': [{
                'name': m.name,
                'description': m.description,
                'reward': m.reward,
                'type': m.type,
            } for m in achieved_milestones],
            'next_milestones': [{
                'name': m.name,
                'description': m.description,
                'reward': m.reward,
                'type': m.type,
            } for m in next_milestones],
            'total_milestones': len(achieved_milestones),  # Total achieved milestones count
        }
        
        return JsonResponse(data, status=200)

    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error if something goes wrong
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Use this temporarily for debugging
def delete_sale(request, sale_id):
    # If you want to handle _method POST -> DELETE override
    if request.method == 'POST' and request.body:
        data = json.loads(request.body)
        if data.get('_method') == 'DELETE':
            # Process the delete operation
            sale = get_object_or_404(Sale, id=sale_id)
            sale.is_archived = True
            sale.save()
            # Update unit status
            unit = sale.unit
            unit.status = 'Available'
            unit.save()

            return JsonResponse({"message": "Sale and unit affiliation deleted successfully"})

    return JsonResponse({"message": "Invalid request"}, status=400)

@csrf_exempt  # Use this temporarily for debugging
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        if customer.archived:
            return JsonResponse({"message": "Customer is already archived"}, status=400)
        
        customer.archived = True
        customer.save()
        return JsonResponse({"message": "Customer archived successfully"}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({"message": "Customer not found"}, status=404)



def sales_by_month(request):
    broker_id = request.GET.get('broker_id')
    year = request.GET.get('year')  # Get the year from the query params

    if not broker_id:
        return JsonResponse({"success": False, "message": "Broker ID is required"}, status=400)

    # If no year is provided, default to the current year
    if not year:
        year = timezone.now().year
    else:
        try:
            year = int(year)  # Ensure the year is an integer
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid year"}, status=400)

    # Get the count of sales grouped by month for a specific broker and year
    sales_filter = Sale.objects.filter(broker_id=broker_id, status='Sold')
    
    # If a year is specified, filter by that year
    if year:
        sales_filter = sales_filter.filter(date_sold__year=year)

    sales_data = sales_filter.annotate(month=ExtractMonth('date_sold')) \
        .values('month') \
        .annotate(sales_count=Count('id')) \
        .order_by('month')

    # Prepare the data for months and sales count
    months = [sale['month'] for sale in sales_data]
    sales_count = [sale['sales_count'] for sale in sales_data]

    # Month names (1 = January, 2 = February, etc.)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Prepare the response data mapping month numbers to their names and sales count
    month_sales = {}
    for month, count in zip(months, sales_count):
        month_sales[month_names[month - 1]] = count  # Adjust month because month is 1-based


    # Get distinct years the broker has made sales
    years = Sale.objects.filter(broker_id=broker_id) \
        .annotate(year=ExtractYear('date_sold')) \
        .values('year') \
        .distinct() \
        .order_by('-year') 

    available_years = [year['year'] for year in years]

    return JsonResponse({
        "success": True,
        "month_sales": month_sales,  # Sales per month
        "years": available_years,  # Available years for the dropdown
    })
