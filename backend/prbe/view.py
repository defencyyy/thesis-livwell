# In brokers/views.py (or the appropriate views file)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from brokers.models import Broker  # Import Broker from the Brokers app
from django.contrib.auth.hashers import check_password  # Import check_password for validating hashed passwords

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')



            # Check if the username and password are received
            if not username or not password:
                return JsonResponse({"success": False, "message": "Missing username or password"}, status=400)

            # Retrieve user from the brokers_broker table
            try:
                broker = Broker.objects.get(username=username)
                

            except Broker.DoesNotExist:
                all_brokers = Broker.objects.all()
                
                return JsonResponse({"success": False, "message": "User does not exist"}, status=404)

            # Validate the password
            if check_password(password, broker.password):  # Use check_password if passwords are hashed
                
                return JsonResponse({"success": True, "message": "Login successful"}, status=200)
            else:
                
                return JsonResponse({"success": False, "message": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=400)
