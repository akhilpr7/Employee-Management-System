from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import (
    LoginAPIView,
    RegisterAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="api_login"),
    path("register/", RegisterAPIView.as_view(), name="api_register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="api_token_refresh"),
    path("profile/", ProfileAPIView.as_view(), name="api_profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="api_change_password"),
    path("logout/", LogoutAPIView.as_view(), name="api_logout"),
]
