# profiles/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_staff', False):
            return True
        return getattr(request.user, 'id', None) == obj.user_id

class IsMentor(permissions.BasePermission):
    """
    Разрешение для пользователей с ролью "MENTOR".
    Ожидается, что в JWT-токене присутствует поле 'role'.
    """
    def has_permission(self, request, view):
        return request.user and getattr(request.user, 'role', None) == 'MENTOR'

class IsMentee(permissions.BasePermission):
    """
    Разрешение для пользователей с ролью "MENTEE".
    Ожидается, что в JWT-токене присутствует поле 'role'.
    """
    def has_permission(self, request, view):
        return request.user and getattr(request.user, 'role', None) == 'MENTEE'