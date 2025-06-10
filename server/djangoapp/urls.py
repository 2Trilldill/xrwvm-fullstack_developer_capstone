from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # ✅ Auth routes
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # ✅ Car model route
    path('get_cars', views.get_cars, name='getcars'),

    # ✅ Dealer-related routes
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),
    path('get_dealer/<int:dealer_id>', views.get_dealer_details, name='get_dealer_details'),
    path('get_reviews/<int:dealer_id>', views.get_dealer_reviews, name='get_dealer_reviews'),

    # ✅ Review post route
    path('add_review', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
