from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permite modificação e exclusão apenas para o criador do objeto."""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user
