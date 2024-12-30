from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permite modificação e exclusão apenas para o criador do post ou no caso de likes, para todos os usuários autenticados."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if view.action == "like":
            return True

        return obj.created_by == request.user
