# session_app/permissions.py
import requests
from django.conf import settings
from rest_framework import permissions

class IsMentor(permissions.BasePermission):
    """Allows access only to users with the MENTOR role or staff."""
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'MENTOR' or getattr(request.user, 'is_staff', False)

class IsMentee(permissions.BasePermission):
    """Allows access only to users with the MENTEE role or staff."""
    def has_permission(self, request, view):
        return getattr(request.user, 'role', None) == 'MENTEE' or getattr(request.user, 'is_staff', False)

class IsOwnerAvailability(permissions.BasePermission):
    """
    Allows edit/delete only if the current user owns the availability (verified via Profile Service)
    or is a staff user.
    """
    def has_object_permission(self, request, view, obj):
        # Staff has full access
        if getattr(request.user, 'is_staff', False):
            return True

        # Check with Profile Service whether the mentor_id belongs to the current user
        profile_url = f"{settings.PROFILE_SERVICE_URL}/api/mentors/{obj.mentor_id}/"
        headers = {}
        auth_header = request.headers.get('Authorization')
        if auth_header:
            headers['Authorization'] = auth_header

        try:
            resp = requests.get(profile_url, headers=headers, timeout=5)
            resp.raise_for_status()
        except Exception:
            return False

        user_id = resp.json().get('user_id')
        return user_id == request.user.id

class IsOwnerSession(permissions.BasePermission):
    """
    Allows mentee to cancel a session and mentor to confirm or decline.
    Staff users can do anything.
    """
    def has_object_permission(self, request, view, obj):
        # Mentee can cancel (DELETE or PATCH to "cancelled")
        if request.user.role == 'MENTEE' and obj.mentee_id == request.user.id:
            return True
        # Mentor can confirm or decline
        if request.user.role == 'MENTOR' and obj.mentor_id == request.user.id:
            return True
        # Staff has full access
        return getattr(request.user, 'is_staff', False)
