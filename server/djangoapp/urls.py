from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views  # ✅ Import views

app_name = 'djangoapp'

urlpatterns = [
    # ✅ Login route
    path(route='login', view=views.login_user, name='login'),

    # 🔜 Logout Route
    path(route='logout', view=views.logout_user, name='logout'),

    # 🔜 Future paths for dealer reviews and add review will be added later

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
