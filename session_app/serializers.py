# sessions_app/serializers.py
from rest_framework import serializers
from .models import Availability, Session
import requests
from django.conf import settings
import logging


logger = logging.getLogger(__name__)
class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'mentor_id', 'start_ts', 'end_ts', 'is_recurring']

    def validate_mentor_id(self, value):
        # Верификация существования ментора в Profile Service
        url = f"{settings.PROFILE_SERVICE_URL}/api/mentors/{value}/"
        headers = {}
        request = self.context.get('request')
        if request:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                headers['Authorization'] = auth_header
        logger.debug(f"[Availability] Validating mentor_id {value}: GET {url} with headers {headers}")
        try:
            resp = requests.get(url, headers=headers, timeout=5)
        except requests.RequestException as e:
            logger.error(f"[Availability] Error contacting Profile Service: {e}")
            raise serializers.ValidationError("Failed to contact Profile Service.", code='service_error')
        logger.debug(f"[Availability] Profile Service response: {resp.status_code} - {resp.text}")
        if resp.status_code == 404:
            raise serializers.ValidationError(f"Mentor with id={value} not found.", code='user_not_found')
        if resp.status_code == 401:
            raise serializers.ValidationError("Unauthorized to access Profile Service.", code='service_unauthorized')
        if resp.status_code != 200:
            raise serializers.ValidationError(f"Profile Service returned {resp.status_code}.", code='service_error')
        return value

    def validate(self, data):
        if data['start_ts'] >= data['end_ts']:
            raise serializers.ValidationError("'start_ts' must be before 'end_ts'.")
        return data


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'mentor_id', 'mentee_id', 'start_ts', 'end_ts', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']

    def _verify_profile(self, value, role):
        url = f"{settings.PROFILE_SERVICE_URL}/api/{role}s/{value}/"
        headers = {}
        request = self.context.get('request')
        if request:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                headers['Authorization'] = auth_header
        logger.debug(f"[Session] Validating {role}_id {value}: GET {url} with headers {headers}")
        try:
            resp = requests.get(url, headers=headers, timeout=5)
        except requests.RequestException as e:
            logger.error(f"[Session] Error contacting Profile Service for {role}: {e}")
            raise serializers.ValidationError(f"Failed to contact Profile Service for {role}.", code='service_error')
        logger.debug(f"[Session] Profile Service response for {role}: {resp.status_code} - {resp.text}")
        if resp.status_code == 404:
            raise serializers.ValidationError({f"{role}_id": f"{role.title()} with id={value} not found."}, code='user_not_found')
        if resp.status_code == 401:
            raise serializers.ValidationError("Unauthorized to access Profile Service.", code='service_unauthorized')
        if resp.status_code != 200:
            raise serializers.ValidationError(f"Profile Service returned {resp.status_code}.", code='service_error')

    def validate_mentor_id(self, value):
        self._verify_profile(value, role='mentor')
        return value

    def validate_mentee_id(self, value):
        self._verify_profile(value, role='mentee')
        return value

    def validate(self, data):
        if data['start_ts'] >= data['end_ts']:
            raise serializers.ValidationError("'start_ts' must be before 'end_ts'.")
        return data