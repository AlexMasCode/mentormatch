# session_app/views.py
from datetime import datetime
import logging
import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from django.conf import settings

from .models import Availability, Session
from .serializers import AvailabilitySerializer, SessionSerializer
from .utils import subtract_intervals
from .permissions import IsMentor, IsMentee, IsOwnerAvailability, IsOwnerSession

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="List availability windows",
        description="Returns pages of availability intervals for the authenticated mentor.",
    ),
    retrieve=extend_schema(
        summary="Retrieve availability window",
        description="Details for a single availability interval by its ID.",
    ),
    create=extend_schema(
        summary="Create availability window",
        description="Create a new availability interval for the authenticated mentor.",
    ),
    update=extend_schema(
        summary="Update availability window",
        description="Full update of an existing availability interval.",
    ),
    partial_update=extend_schema(
        summary="Partially update availability window",
        description="Modify one or more fields of an availability interval.",
    ),
    destroy=extend_schema(
        summary="Delete availability window",
        description="Remove an availability interval by its ID.",
    ),
)
class AvailabilityViewSet(viewsets.ModelViewSet):
    """
    Manage availability windows for mentors.
    list/retrieve: any authenticated user (filtered to own when role=MENTOR).
    create/update/delete: only mentors can manage their own windows.
    """
    serializer_class = AvailabilitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['mentor_id', 'start_ts', 'end_ts']
    ordering_fields = ['start_ts']

    def get_mentor_profile_id(self):
        """Fetch mentor_profile.id from Profile Service using user_id."""
        user = self.request.user
        url = f"{settings.PROFILE_SERVICE_URL}/api/mentors/?user_id={user.id}"
        headers = {}
        auth = self.request.headers.get('Authorization')
        if auth:
            headers['Authorization'] = auth
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()
            results = resp.json().get('results', [])
            # Find the profile where user_id matches exactly
            for profile in results:
                if profile.get('user_id') == user.id:
                    return profile.get('id')
            return None
        except Exception as e:
            logger.error(f"Error fetching mentor profile id: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching mentor profile id: {e}")
            return None


    def get_queryset(self):
        qs = Availability.objects.all()
        user = self.request.user
        if getattr(user, 'is_staff', False):
            return qs
        if getattr(user, 'role', None) == 'MENTOR':
            pid = self.get_mentor_profile_id()
            if pid:
                return qs.filter(mentor_id=pid)
        return qs.none()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsMentor()]
        return [IsAuthenticated(), IsMentor(), IsOwnerAvailability()]

    def perform_create(self, serializer):
        """
        Automatically assign mentor_id from Profile Service.
        """
        pid = self.get_mentor_profile_id()
        serializer.save(mentor_id=pid)


@extend_schema_view(
    list=extend_schema(
        summary="List sessions",
        description="List all sessions for the authenticated user (mentor or mentee).",
    ),
    retrieve=extend_schema(
        summary="Retrieve session",
        description="Get details of a single session by its ID.",
    ),
    create=extend_schema(
        summary="Request a session",
        description="Mentee requests a new mentorship session (status=pending).",
    ),
    partial_update=extend_schema(
        summary="Update session status",
        description="Mentee can cancel (status=cancelled), mentor can confirm/decline.",
    ),
    destroy=extend_schema(
        summary="Delete session",
        description="Mentee or admin can delete a session (before confirmation).",
    ),
    free_slots=extend_schema(
        summary="List free slots",
        description="Return free availability intervals for a given mentor, subtracting busy sessions.",
        parameters=[
            OpenApiParameter('mentor_id', OpenApiParameter.PATH, description="ID of the mentor"),
            OpenApiParameter('date_from', OpenApiParameter.QUERY, description="ISO datetime start filter", required=False),
            OpenApiParameter('date_to', OpenApiParameter.QUERY, description="ISO datetime end filter", required=False),
        ],
    ),
)
class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['mentor_id', 'mentee_id', 'status']
    ordering_fields = ['start_ts']

    def get_mentor_profile_id(self):
        user = self.request.user
        url = f"{settings.PROFILE_SERVICE_URL}/api/mentors/"
        headers = {}
        if auth := self.request.headers.get("Authorization"):
            headers["Authorization"] = auth
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        for profile in resp.json().get('results', []):
            if profile.get('user_id') == user.id:
                return profile.get('id')
        return None

    def get_mentee_profile_id(self):
        user = self.request.user
        url = f"{settings.PROFILE_SERVICE_URL}/api/mentees/me/"
        headers = {}
        if auth := self.request.headers.get("Authorization"):
            headers["Authorization"] = auth

        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data.get("id")

    def get_queryset(self):
        qs = Session.objects.all()
        user = self.request.user
        if user.is_staff:
            return qs
        if user.role == 'MENTOR':
            pid = self.get_mentor_profile_id()
            return qs.filter(mentor_id=pid) if pid else qs.none()
        if user.role == 'MENTEE':
            pid = self.get_mentee_profile_id()
            return qs.filter(mentee_id=pid) if pid else qs.none()
        return qs.none()

    def get_permissions(self):
        if self.action == 'free_slots':
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsMentee()]
        if self.action in ['partial_update', 'update', 'destroy']:
            return [IsAuthenticated(), IsOwnerSession()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        mentee_pid = self.get_mentee_profile_id()
        logger.debug(f"[perform_create] mentee_pid resolved as: {mentee_pid}")
        mentor_id = serializer.validated_data.get('mentor_id')
        serializer.save(mentor_id=mentor_id, mentee_id=mentee_pid)

    @action(detail=False, methods=['get'], url_path='free-slots/(?P<mentor_id>[^/.]+)')
    def free_slots(self, request, mentor_id=None):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        try:
            from_dt = datetime.fromisoformat(date_from) if date_from else None
            to_dt = datetime.fromisoformat(date_to) if date_to else None
        except ValueError:
            return Response({'detail': 'Invalid date format.'}, status=status.HTTP_400_BAD_REQUEST)

        avail_qs = Availability.objects.filter(mentor_id=mentor_id)
        if from_dt:
            avail_qs = avail_qs.filter(end_ts__gt=from_dt)
        if to_dt:
            avail_qs = avail_qs.filter(start_ts__lt=to_dt)
        avail_list = [(a.start_ts, a.end_ts) for a in avail_qs]

        busy_qs = Session.objects.filter(
            mentor_id=mentor_id,
            status__in=[Session.STATUS_PENDING, Session.STATUS_CONFIRMED]
        )
        if from_dt:
            busy_qs = busy_qs.filter(end_ts__gt=from_dt)
        if to_dt:
            busy_qs = busy_qs.filter(start_ts__lt=to_dt)
        busy_list = [(s.start_ts, s.end_ts) for s in busy_qs]

        free = subtract_intervals(avail_list, busy_list)
        data = [{'start': s.isoformat(), 'end': e.isoformat()} for s, e in free]
        return Response(data)

