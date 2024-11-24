from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    path("", include(router.urls)),
]
