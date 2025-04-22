from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models

from session_app.models import Session
from .models import MentorReview, MenteeRating
from .serializers import MentorReviewSerializer, MenteeRatingSerializer
from .permissions import IsSessionMentee, IsSessionMentor, get_profile_id
from ratings.kafka.kafka_producer import send_rating_update
from rest_framework.permissions import IsAuthenticated

class MentorReviewViewSet(viewsets.ModelViewSet):
    queryset = MentorReview.objects.all().order_by('-created_at')
    serializer_class = MentorReviewSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'score']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsSessionMentee()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # 1. Check that session belongs to this mentee
        session_id = request.data.get('session')
        try:
            session = Session.objects.get(pk=session_id)
        except Session.DoesNotExist:
            return Response({"detail": "Session not found."}, status=404)

        mentee_profile_id = get_profile_id(request, role="mentees")
        if session.mentee_id != mentee_profile_id:
            raise PermissionDenied("You can only review your own sessions.")

        # 2. Serialize and save
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(
            mentor_id=session.mentor_id,
            mentee_id=session.mentee_id
        )

        #3. Recalculate the rating and send to Kafka
        avg = MentorReview.objects.filter(mentor_id=session.mentor_id)\
               .aggregate(models.Avg("score"))["score__avg"] or 0
        send_rating_update(session.mentor_id, round(avg, 2))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MenteeRatingViewSet(viewsets.ModelViewSet):
    queryset = MenteeRating.objects.all().order_by('-date')
    serializer_class = MenteeRatingSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['date', 'score']
    ordering = ['-date']

    def get_permissions(self):
        if self.action == 'create':
            return [IsSessionMentor()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        session = serializer.validated_data['session']
        serializer.save(
            mentor_id=session.mentor_id,
            mentee_id=session.mentee_id
        )
