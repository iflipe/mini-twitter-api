from django.urls import path
from .views import CreateUserAPIView, LoginUserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mini-Twitter API",
        default_version="v1",
        description="Uma API para uma versão simplificada de uma rede social no estilo do Twitter, com autenticação via JWT, com endpoints para registro e login de usuários, e CRUD de posts, com funcionalidades de resposta a posts e a curtidas.",
        contact=openapi.Contact(email="foo@bar.com"),
        license=openapi.License(name="Open Source"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("register/", CreateUserAPIView.as_view(), name="register"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
