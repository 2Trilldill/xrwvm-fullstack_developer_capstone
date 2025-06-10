from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django app backend API routes (e.g., login_user, logout_user)
    path('djangoapp/', include('djangoapp.urls')),

    # React frontend routes (served via index.html)
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),  

    # Static HTML templates (served normally)
    path('', TemplateView.as_view(template_name="Home.html"), name='home'),
    path('about/', TemplateView.as_view(template_name="About.html"), name='about'),
    path('contact/', TemplateView.as_view(template_name="Contact.html"), name='contact'),
]

# Static/media files config
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
