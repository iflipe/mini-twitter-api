from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, PostDetailSerializer
from .models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("replies")
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if self.action in ["retrieve", "update", "partial_update"]:
            serializer_class = PostDetailSerializer
        else:
            serializer_class = PostSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)
