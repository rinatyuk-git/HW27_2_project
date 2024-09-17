from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Проверка на Модератора."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):
    """Проверка на Создателя."""
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
