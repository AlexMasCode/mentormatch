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
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, 'is_staff', False):
            return True

        if request.user.role == 'MENTEE':
            resp = requests.get(
                f"{settings.PROFILE_SERVICE_URL}/api/mentees/me/",
                headers={'Authorization': request.headers.get('Authorization')},
                timeout=5
            )
            resp.raise_for_status()
            profile_id = resp.json().get('id')
            return obj.mentee_id == profile_id

        if request.user.role == 'MENTOR':
            resp = requests.get(
                f"{settings.PROFILE_SERVICE_URL}/api/mentors/?user_id={request.user.id}",
                headers={'Authorization': request.headers.get('Authorization')},
                timeout=5
            )
            resp.raise_for_status()
            results = resp.json().get('results', [])
            mentor_profile_id = results[0]['id'] if results else None
            return obj.mentor_id == mentor_profile_id

        return False

