from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Availability, Session
from .serializers import AvailabilitySerializer, SessionSerializer
from .utils import subtract_intervals
from datetime import datetime


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['mentor_id', 'start_ts', 'end_ts']
    ordering_fields = ['start_ts']

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['mentor_id', 'mentee_id', 'status']
    ordering_fields = ['start_ts']

    @action(detail=False, methods=['get'], url_path='free-slots/(?P<mentor_id>[^/.]+)')
    def free_slots(self, request, mentor_id=None):
        # parse date_from & date_to query params
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