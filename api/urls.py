from django.urls import path
from .views import CreateUserAPIView, LoginUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="register"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
