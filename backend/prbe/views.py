# Django Lib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from companies.serializers import CompanySerializer
from developers.models import Developer
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from collections import Counter
import os




from brokers.models import Broker 
from customers.models import Customer
from sales.models import Sale
from units.models import Unit, UnitImage
from sites.models import Site
from salesdetails.models import SalesDetails
from documents.models import DocumentType, Document

 
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

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

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

@csrf_exempt  # This decorator is optional if you are using CSRF tokens correctly in your request
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
                affiliated_link=data.get('affiliated_link', ''),  # optional field
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
        # Fetch sites that are either 'preselling' or 'completed' and have available units
        sites = Site.objects.filter(status__in=['preselling', 'completed'])
        
        site_data = []
        for site in sites:
            # Check if there are any available units for this site
            available_units = Unit.objects.filter(site=site, status='available')
            if available_units.exists():  # Only add the site if there are available units
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
                # Fetch all images associated with this unit using the UnitImage model
                images = UnitImage.objects.filter(unit_id=unit.id)

                    
                # Get URLs for all images
                image_urls = [request.build_absolute_uri(image.image.url) for image in images]

                unit_data.append({
                    'id': unit.id,
                    'unit_title': unit.unit_title,
                    'images': image_urls,  # List of image URLs
                    'price': unit.price,
                    'bedroom': unit.bedroom,
                    'bathroom': unit.bathroom,
                    'floor_area': unit.floor_area,
                    'floor': unit.floor,
                    'balcony': unit.balcony,
                    'view': unit.view,
                    'company_id': unit.company.id,  # Add the company_id to the response
                    
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
        total_customers = customers.count()  # Get the total number of customers
        customer_data = []
        for customer in customers:
            # Basic customer info
            customer_name = f"{customer.first_name} {customer.last_name}"
            contact_number = customer.contact_number
            company_id = customer.company.id  # Get the company ID associated with the customer

            # If include_sales is True, fetch sales and related data
            if include_sales:
                sales = Sale.objects.filter(customer_id=customer.id)
                if sales.exists():
                    # For each sale, get the related site and unit
                    for sale in sales:
                        site = Site.objects.get(id=sale.site_id)
                        unit = Unit.objects.get(id=sale.unit_id)

                        customer_data.append({
                            'id': customer.id,
                            'customer_name': customer_name,
                            'contact_number': contact_number,
                            'site': site.name,
                            'unit': unit.unit_title,
                            'company_id': company_id,  # Add company ID
                            'document_status': "Pending",  # Adjust document status as needed
                        })
                else:
                    customer_data.append({
                        'id': customer.id,
                        'customer_name': customer_name,
                        'contact_number': contact_number,
                        'site': "To be followed",
                        'unit': "To be followed",
                        'company_id': company_id,  # Add company ID
                        'document_status': "Pending",
                    })
            else:
                # If no sales data, return just basic info (id and name)
                customer_data.append({
                    'id': customer.id,
                    'name': customer_name,
                    'contact_number': contact_number,
                    'company_id': company_id,  # Add company ID
                })

        # Return the total customer count and the customer data
        return JsonResponse({
            'success': True,
            'total_customers': total_customers,  # Return the total number of customers
            'customers': customer_data
        }, status=200)

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
def fetch_sales(request):
    try:
        broker_id = request.GET.get('broker_id')

        # Fetch sales based on the broker_id, if provided
        if broker_id:
            sales = Sale.objects.filter(broker__id=broker_id).select_related(
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
            # Add sale data to the list, including IDs and other relevant information
            sales_data.append({
                'customer_name': f"{sale.customer.first_name} {sale.customer.last_name}",
                'customer_id': sale.customer.id,   # customer_id
                'site_name': sale.site.name,
                'site_id': sale.site.id,           # site_id
                'unit_title': sale.unit.unit_title,
                'unit_id': sale.unit.id,           # unit_id
                'price': sale.unit.price,
                'status': sale.status,
                'email': sale.customer.email,
                'broker_id': sale.broker.id if sale.broker else None, # broker_id
                'broker_name': f"{sale.broker.first_name} {sale.broker.last_name}" if sale.broker else None,  # broker_name     
            })      
         # Group the sales by status and count occurrences
        status_count = Counter(sale.status for sale in sales)

        # Prepare the data to send to the frontend
        sales_status_data = {
            'sold': status_count.get('sold', 0),
            'pending': status_count.get('pending reservation', 0),
            'reserved': status_count.get('reserved', 0),
        }
        return JsonResponse({'success': True, 'sales': sales_data, 'sales_status_data': sales_status_data}, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
def reserve_unit(request):
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
                status='pending reservation',  # Set to pending reservation
                reservation_fee=payment_amount,
                payment_method=payment_method,
                payment_reference=payment_reference,
                reservation_file=reservation_file if reservation_file else None
            )

            # Update the unit status to pending_reservation
            unit.status = 'pending reservation'
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

    # Prepare the response data with all related information
    sales_detail_data = {
        'uuid': sales_detail_id,  # Use uuid here instead of id
        'id':sales_detail.id,
        'customer_id': sales_detail.customer_id,
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
        'unit_name': unit.unit_title  # Unit title
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

# Fetch document types - for dropdown
def fetch_document_types(request):
    try:
        document_types = DocumentType.objects.all()
        document_types_data = [
            {"id": dt.id, "name": dt.name, "description": dt.description}
            for dt in document_types
        ]
        return JsonResponse({"success": True, "documentTypes": document_types_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

# Upload document for a customer
@csrf_exempt
def upload_document(request):
    if request.method == "POST":
        # Get the common fields from the request
        customer_id = request.POST.get("customer")
        company_id = request.POST.get("company")
        object_id = request.POST.get("object_id", 1)  # Default value of 1 if not provided
        content_id = request.POST.get("content_id", 1)  # Default value of 1 if not provided

        # Get the list of files and document types
        files = request.FILES.getlist("files[]")
        document_type_ids = request.POST.getlist("document_types[]")

        # Validate that customer_id, document_type_ids, and files are provided
        if not customer_id or not document_type_ids or not files:
            return JsonResponse({"success": False, "message": "Missing required fields."}, status=400)

        try:
            # Get the customer object
            customer = get_object_or_404(Customer, id=customer_id)

            # Loop over the files and their corresponding document types
            for i, file in enumerate(files):
                document_type_id = document_type_ids[i] if i < len(document_type_ids) else document_type_ids[0]  # Default to first doc type if out of bounds
                document_type = get_object_or_404(DocumentType, id=document_type_id)

                # Check if a document already exists for this customer and document type
                existing_document = Document.objects.filter(
                    customer_id=customer_id, document_type=document_type
                ).first()

                if existing_document:
                    # If the document already exists, update it with the new file
                    existing_document.file = file
                    existing_document.save()
                else:
                    # If the document doesn't exist, create a new document
                    Document.objects.create(
                        customer_id=customer_id,
                        document_type=document_type,
                        company_id=company_id,
                        file=file,
                        object_id=object_id,  # Pass the object_id
                        content_type_id=content_id,  # Pass the content_id
                    )

            return JsonResponse({"success": True, "message": "Documents uploaded successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

# Fetch documents for a given customer
@csrf_exempt
def fetch_customer_documents(request, customer_id):
    try:
        # Get the customer by ID
        customer = Customer.objects.get(id=customer_id)

        # Fetch documents for the customer, grouped by document type
        documents = Document.objects.filter(customer=customer)

        # Prepare a list to return
        document_data = []
        for doc in documents:
            document_data.append({
                'id': doc.id,
                'document_type_id': doc.document_type.id,
                'document_type_name': doc.document_type.name,
                'file_name':os.path.basename(doc.file.name),
                'uploaded_at': doc.uploaded_at.isoformat(),
            })

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
        return JsonResponse({
            'success': False,
            'message': str(e),
        }, status=500)

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

@csrf_exempt
def company_edit(request):
    try:
        developer_id = request.headers.get("Developer-ID")
        company_description = request.POST.get("description")
        company_logo = request.FILES.get("logo")

        if not developer_id:
            return JsonResponse({"success": False, "message": "Developer ID not provided"}, status=400)

        developer = get_object_or_404(Developer, id=developer_id)
        company = developer.company

        # Prepare data with only non-null fields
        data = {}
        if company_description is not None:
            data["description"] = company_description
        if company_logo is not None:
            data["logo"] = company_logo

        # Debugging info
        logger.debug(f"Updating with data: {data}")

        # Pass the existing company instance and partial data to the serializer
        serializer = CompanySerializer(company, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "message": "Company updated successfully"}, status=200)
        else:
            # Log validation errors
            logger.error(f"Validation errors: {serializer.errors}")
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    except Exception as e:
        logger.exception("Error updating company")
        return JsonResponse({"success": False, "message": "An unexpected error occurred"}, status=500)
