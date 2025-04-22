import requests
from django.conf import settings
from rest_framework import permissions

class IsSessionMentee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MENTEE" or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.session.mentee_id == get_profile_id(request, role="mentees")

class IsSessionMentor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "MENTOR" or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.session.mentor_id == get_profile_id(request, role="mentors")

def get_profile_id(request, role):
    url = f"{settings.PROFILE_SERVICE_URL}/api/{role}/me/" if role == "mentees" else f"{settings.PROFILE_SERVICE_URL}/api/{role}/?user_id={request.user.id}"
    headers = {"Authorization": request.headers.get("Authorization", "")}
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if role=="mentees":
        return data.get("id")
    return data.get("results", [{}])[0].get("id")
