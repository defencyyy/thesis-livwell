from django.http import JsonResponse
from django.views import View
from developers.models import Developer
from .models import Company
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
import logging

# Set up logging
logger = logging.getLogger(__name__)

class CompanyView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        logger.debug(f"GET request received with Developer-ID: {developer_id} and Company-ID: {company_id}")

        if not developer_id or not company_id:
            logger.error("Developer ID or Company ID not provided")
            return JsonResponse({'error': 'Developer ID or Company ID not provided'}, status=400)

        try:
            developer = Developer.objects.get(id=developer_id)
            company = Company.objects.get(id=company_id)

            if developer.company.id == company.id:
                # Set cookies with SameSite=None and Secure=True
                refresh = RefreshToken.for_user(developer)
                access_token = str(refresh.access_token)

                response = JsonResponse({
                    'company_name': company.name,
                    'company_description': company.description,
                    'company_logo': company.logo.url if company.logo else None
                })

                # Set the cookies with SameSite=None and Secure=True
                response.set_cookie(
                    'access_token', access_token, httponly=True, max_age=900, samesite='None', secure=True
                )
                response.set_cookie(
                    'refresh_token', str(refresh), httponly=True, max_age=86400, samesite='None', secure=True
                )

                # Set CSRF token in response headers
                csrf_token = get_token(request)
                response["X-CSRFToken"] = csrf_token
                logger.debug(f"CSRF token set in response: {csrf_token}")
                return response
            else:
                logger.warning("Unauthorized access attempt")
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        except Developer.DoesNotExist:
            logger.error("Developer not found")
            return JsonResponse({'error': 'Developer not found'}, status=404)
        except Company.DoesNotExist:
            logger.error("Company not found")
            return JsonResponse({'error': 'Company not found'}, status=404)

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        logger.debug(f"PUT request received with Developer-ID: {developer_id} and Company-ID: {company_id}")

        if not developer_id or not company_id:
            logger.error("Developer ID or Company ID not provided")
            return JsonResponse({'error': 'Developer ID or Company ID not provided'}, status=400)

        try:
            developer = Developer.objects.get(id=developer_id)
            company = Company.objects.get(id=company_id)

            if developer.company.id == company.id:
                # Log parsing form data
                parser = MultiPartParser()
                data = parser.parse(request)

                description = data.data.get('description')
                logo = data.files.get('logo')

                logger.debug(f"Updating company with description: {description} and logo: {logo}")

                if description:
                    company.description = description
                if logo:
                    company.logo = logo

                company.save()
                logger.info("Company updated successfully")
                return JsonResponse({'message': 'Company updated successfully'})

            else:
                logger.warning("Unauthorized access attempt")
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        except Developer.DoesNotExist:
            logger.error("Developer not found")
            return JsonResponse({'error': 'Developer not found'}, status=404)
        except Company.DoesNotExist:
            logger.error("Company not found")
            return JsonResponse({'error': 'Company not found'}, status=404)
