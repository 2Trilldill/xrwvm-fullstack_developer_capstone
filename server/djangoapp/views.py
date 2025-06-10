from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel  
from .populate import initiate          
import logging
import json

# Logger setup
logger = logging.getLogger(__name__)

# ✅ LOGIN VIEW
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"status": "Invalid"}, status=401)
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    return JsonResponse({"status": "Invalid method"}, status=405)

# ✅ LOGOUT VIEW
@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

# ✅ REGISTRATION VIEW
@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("userName")
            password = data.get("password")
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            email = data.get("email")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"}, status=400)

            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            return JsonResponse({"userName": username, "status": "Registered"})

        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    return JsonResponse({"status": "Invalid method"}, status=405)

# ✅ GET CARS VIEW
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})

