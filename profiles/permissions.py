# profiles/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_staff', False):
            return True
        return getattr(request.user, 'id', None) == obj.user_id
