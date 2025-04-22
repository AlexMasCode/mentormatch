from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import MentorReview, MenteeRating
from ratings.permissions import get_profile_id

class MentorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorReview
        fields = ["id", "session", "mentor_id", "mentee_id", "score", "comment", "created_at"]
        read_only_fields = ["id", "mentor_id", "mentee_id", "created_at"]

    def validate_session(self, session_obj):
        request = self.context['request']
        # get the “profile id” of the logged‑in mentee, exactly as you do in the view
        mentee_profile_id = get_profile_id(request, role="mentees")
        if session_obj.mentee_id != mentee_profile_id:
            raise PermissionDenied("You can only review your own sessions.")
        return session_obj

class MenteeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenteeRating
        fields = ["id", "session", "mentor_id", "mentee_id", "score", "feedback", "date"]
        read_only_fields = ["id", "mentor_id", "mentee_id", "date"]
