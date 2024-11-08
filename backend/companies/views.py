from django.http import JsonResponse
from django.views import View  # Import View class for CBVs
from developers.models import Developer
from .models import Company

class CompanyView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the developer and company IDs from the headers
        developer_id = request.headers.get('Developer-ID')
        company_id = request.headers.get('Company-ID')

        # If developer_id or company_id is not provided, return an error
        if not developer_id or not company_id:
            return JsonResponse({'error': 'Developer ID or Company ID not provided'}, status=400)

        try:
            # Fetch the developer and associated company
            developer = Developer.objects.get(id=developer_id)
            company = Company.objects.get(id=company_id)

            # Check if the developer is associated with the company
            if developer.company.id == company.id:
                return JsonResponse({
                    'company_name': company.name,
                    'company_description': company.description,
                    'company_logo': company.logo.url if company.logo else None  # Return logo URL if it exists
                })
            else:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        except Developer.DoesNotExist:
            return JsonResponse({'error': 'Developer not found'}, status=404)
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
