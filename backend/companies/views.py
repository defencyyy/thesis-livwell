from django.http import JsonResponse
from django.views import View
from developers.models import Developer
from .models import Company
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import QueryDict

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.http import QueryDict
from rest_framework.parsers import MultiPartParser, FormParser

class CompanyView(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        if not developer_id or not company_id:
            return JsonResponse({'error': 'Developer ID or Company ID not provided'}, status=400)

        try:
            developer = Developer.objects.get(id=developer_id)
            company = Company.objects.get(id=company_id)

            if developer.company.id == company.id:
                return JsonResponse({
                    'company_name': company.name,
                    'company_description': company.description,
                    'company_logo': company.logo.url if company.logo else None
                })
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        except Developer.DoesNotExist:
            return JsonResponse({'error': 'Developer not found'}, status=404)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)

    @method_decorator(ensure_csrf_cookie)
    def put(self, request, *args, **kwargs):
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        if not developer_id or not company_id:
            return JsonResponse({'error': 'Developer ID or Company ID not provided'}, status=400)

        try:
            developer = Developer.objects.get(id=developer_id)
            company = Company.objects.get(id=company_id)

            if developer.company.id == company.id:
                # Use MultiPartParser to handle form-data
                parser = MultiPartParser()  # Use this for handling file uploads
                data = parser.parse(request)

                # The description and logo come from the parsed data
                description = data.data.get('description')
                logo = data.files.get('logo')

                if description:
                    company.description = description
                if logo:
                    company.logo = logo

                company.save()
                return JsonResponse({'message': 'Company updated successfully'})

            else:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        except Developer.DoesNotExist:
            return JsonResponse({'error': 'Developer not found'}, status=404)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
