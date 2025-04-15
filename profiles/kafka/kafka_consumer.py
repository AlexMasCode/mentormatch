# profile_service/kafka_consumer.py
import os
import json
from kafka import KafkaConsumer

# Django setup – for accessing models
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "profile_service.settings")
django.setup()

from profiles.models import MentorProfile, MenteeProfile

# Read broker and topic settings from environment variables
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC_NEW_USER = os.environ.get("KAFKA_TOPIC_NEW_USER", "new_user_topic")

consumer = KafkaConsumer(
    TOPIC_NEW_USER,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='profile_service_group',
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Profile Service Kafka consumer started. Listening for new user events...")

for message in consumer:
    event = message.value
    user_id = event.get("user_id")
    role = event.get("role")
    print(f"Received event for user_id: {user_id} with role: {role}")

    # Check if the profile already exists, and create it if not
    if role == "MENTOR":
        if not MentorProfile.objects.filter(user_id=user_id).exists():
            MentorProfile.objects.create(user_id=user_id, bio="", experience_years=0)
            print(f"Created MentorProfile for user {user_id}")
    elif role == "MENTEE":
        if not MenteeProfile.objects.filter(user_id=user_id).exists():
            MenteeProfile.objects.create(user_id=user_id)
            print(f"Created MenteeProfile for user {user_id}")
    else:
        print(f"Unknown role {role} for user {user_id}")
