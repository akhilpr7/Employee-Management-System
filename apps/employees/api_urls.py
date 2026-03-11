from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import FormTemplateViewSet, EmployeeViewSet

router = DefaultRouter()
router.register("forms", FormTemplateViewSet, basename="api_forms")
router.register("employees", EmployeeViewSet, basename="api_employees")

urlpatterns = [
    path("", include(router.urls)),
]
