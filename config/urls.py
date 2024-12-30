from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet

from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_URL_PATH = os.environ.get("ADMIN_URL_PATH")

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")


urlpatterns = [
    path(ADMIN_URL_PATH, admin.site.urls),
    path("", include("api.urls")),
    path("", include(router.urls)),
]
