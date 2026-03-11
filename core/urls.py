from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("employees/", include("apps.employees.urls", namespace="employees")),
    path("", RedirectView.as_view(url="/employees/", permanent=False)),
    # REST API
    path("api/auth/", include("apps.accounts.api_urls")),
    path("api/", include("apps.employees.api_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
