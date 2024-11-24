from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsOwnerOrReadOnly
from .paginations import TimelinePagination
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    UserSerializer,
)
from .models import Post
from .utils import get_tokens_for_user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.order_by("-created_at").prefetch_related("replies")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = TimelinePagination

    def get_serializer(self, *args, **kwargs):
        if self.action in ["retrieve", "update", "partial_update"]:
            serializer_class = PostDetailSerializer
        else:
            serializer_class = PostSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                {"detail": "Usuário já está logado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        data["tokens"] = get_tokens_for_user(user)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LoginUserAPIView(TokenObtainPairView):
    """Retorna conjunto de tokens para usuário caso credenciais estejam corretas."""

    permission_classes = [AllowAny]
