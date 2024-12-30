from django.urls import path
from .views import (
    CreateUserAPIView,
    LoginUserAPIView,
    TokenRefreshAPIView,
    LogoutUserAPIView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mini-Twitter API",
        default_version="v1",
        description="""
        O mini-twitter-api é uma API REST simples que simula algumas funcionalidades básicas do Twitter/X.

        Essa API possui endpoints que permitem ao usuário **criar** e **acessar** sua conta para que possa **ler**, **criar**, **editar**, **curtir** e **deletar** posts.
        """,
        contact=openapi.Contact(email="foo@bar.com"),
        license=openapi.License(name="Open Source"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="register"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("logout/", LogoutUserAPIView.as_view(), name="logout"),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("docs<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
