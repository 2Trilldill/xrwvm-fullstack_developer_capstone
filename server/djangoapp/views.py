from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
import logging
import json

# Logger setup
logger = logging.getLogger(__name__)

# ---------------------------
# ✅ LOGIN VIEW
# ---------------------------
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            return JsonResponse({"status": "Invalid"}, status=401)
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    return JsonResponse({"status": "Invalid method"}, status=405)

# ---------------------------
# ✅ LOGOUT VIEW
# ---------------------------
@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

# ---------------------------
# ✅ REGISTRATION VIEW
# ---------------------------
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

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Registered"})
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=500)
    return JsonResponse({"status": "Invalid method"}, status=405)

# ---------------------------
# ✅ GET CARS VIEW
# ---------------------------
def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": cm.name, "CarMake": cm.car_make.name}
        for cm in car_models
    ]
    return JsonResponse({"CarModels": cars})

# ---------------------------
# ✅ GET DEALERSHIPS VIEW
# ---------------------------
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# ---------------------------
# ✅ GET DEALER DETAILS VIEW
# ---------------------------
def get_dealer_details(request, dealer_id):
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer = get_request(endpoint)
    return JsonResponse({"dealer": dealer})

# ---------------------------
# ✅ GET REVIEWS WITH SENTIMENT
# ---------------------------
def get_dealer_reviews(request, dealer_id):
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    for review in reviews:
        text = review.get("review", "")
        sentiment = analyze_review_sentiments(text)
        review["sentiment"] = sentiment.get("label", "neutral")
    return JsonResponse({"reviews": reviews})

# ---------------------------
# ✅ POST A REVIEW VIEW
# ---------------------------
@csrf_exempt
def add_review(request):
    if request.user.is_anonymous is False:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            return JsonResponse({"status": 200, "message": "Review posted", "response": response})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

