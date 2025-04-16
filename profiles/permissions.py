# profiles/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_staff', False):
            return True
        return getattr(request.user, 'id', None) == obj.user_id

class IsMentor(permissions.BasePermission):
    """
    Permission for users with the "MENTOR" role.
    It is expected that the JWT token contains the 'role' field.
    """
    def has_permission(self, request, view):
        return request.user and getattr(request.user, 'role', None) == 'MENTOR'

class IsMentee(permissions.BasePermission):
    """
    Permission for users with the "MENTEE" role.
    It is expected that the JWT token contains the 'role' field.
    """
    def has_permission(self, request, view):
        return request.user and getattr(request.user, 'role', None) == 'MENTEE'


class IsMentorOrAdmin(permissions.BasePermission):
    """
    Allows access only to users with role 'MENTOR' or admins (is_staff).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and (getattr(user, 'role', None) == 'MENTOR' or user.is_staff))