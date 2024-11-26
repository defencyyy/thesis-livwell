import os
import json
from django.http import JsonResponse

def get_location_data(request):
    """Serve the PhilippinesLocation JSON data."""
    json_path = os.path.join(os.path.dirname(__file__), 'PhilippineGeography.json')
    
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
