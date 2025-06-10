from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
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

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Already Registered"}, status=400)

            # Create new user and log them in
            user = User.objects.create_user(username=username, password=password,
                                            first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            return JsonResponse({"userName": username, "status": "Registered"})

        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    return JsonResponse({"status": "Invalid method"}, status=405)

# 🔜 Future views for dealership functionality
# def get_dealerships(request): ...
# def get_dealer_reviews(request, dealer_id): ...
# def get_dealer_details(request, dealer_id): ...
# def add_review(request): ...
