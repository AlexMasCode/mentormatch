from rest_framework import serializers
from .models import Availability, Session
import requests
from django.conf import settings
import logging


logger = logging.getLogger(__name__)
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'mentor_id', 'start_ts', 'end_ts', 'is_recurring', 'is_booked']
        read_only_fields = ['id', 'mentor_id', 'is_booked']

    def validate(self, data):
        start_ts = data.get('start_ts', getattr(self.instance, 'start_ts', None))
        end_ts = data.get('end_ts',   getattr(self.instance, 'end_ts',   None))

        if start_ts is not None and end_ts is not None and start_ts >= end_ts:
            raise serializers.ValidationError("'start_ts' must be before 'end_ts'.")
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'mentor_id', 'mentee_id', 'start_ts', 'end_ts', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'mentee_id']

    def _verify_profile(self, value, role):
        url = f"{settings.PROFILE_SERVICE_URL}/api/{role}s/{value}/"
        headers = {}
        req = self.context.get('request')
        if req and (auth := req.headers.get('Authorization')):
            headers['Authorization'] = auth
        try:
            resp = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error contacting Profile Service for {role}: {e}")
            raise serializers.ValidationError(f"Failed to contact Profile Service for {role}.")
        if resp.status_code != 200:
            raise serializers.ValidationError(f"Profile Service returned {resp.status_code}.")

    def validate_mentor_id(self, value):
        self._verify_profile(value, role='mentor')
        return value

    def validate(self, data):
        start_ts = data.get('start_ts')
        end_ts   = data.get('end_ts')
        mentor_id = data.get('mentor_id')


        if start_ts and end_ts and start_ts >= end_ts:
            raise serializers.ValidationError("'start_ts' must be before 'end_ts'.")

        if mentor_id and start_ts and end_ts:
            exists = Availability.objects.filter(
                mentor_id=mentor_id,
                start_ts=start_ts,
                end_ts=end_ts,
                is_booked=False
            ).exists()
            if not exists:
                raise serializers.ValidationError(
                    "Session must exactly match an available time slot."
                )

        return data