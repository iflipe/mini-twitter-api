from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsOwnerOrReadOnly
from .paginations import TimelinePagination
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    UserSerializer,
    LikePostSerializer,
)
from .models import Post
from .utils import get_tokens_for_user


class PostViewSet(viewsets.ModelViewSet):
    """Viewset que integra os endpoints de CRUD dos posts, bem como as ações extras de responder e curtir posts"""

    queryset = Post.objects.order_by("-created_at").prefetch_related("replies")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = TimelinePagination

    def get_serializer(self, *args, **kwargs):
        if self.action in ["retrieve", "update", "partial_update"]:
            serializer_class = PostDetailSerializer
        elif self.action == "like":
            serializer_class = LikePostSerializer
        else:
            serializer_class = PostSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=True, methods=["post"])
    def reply(self, request, pk=None):
        """Adiciona um post como resposta ao post ao qual a url faz referência usando o usuário logado, levanta uma exceção para o caso de o post referenciado não existir."""
        context = self.get_serializer_context()
        context["reply_to_id"] = self.kwargs["pk"]
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["post", "delete"])
    def like(self, request, pk=None):
        """Adiciona ou remove uma curtida ao post referenciado caso esse exista ou gera uma exceção."""
        self.permission_classes = [IsAuthenticated]
        context = self.get_serializer_context()
        context["action"] = self.action
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True, context=context
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class CreateUserAPIView(generics.CreateAPIView):
    """Registra um novo usuário com os parâmetros e retorna um par de tokens"""

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
