import json
from kafka import KafkaConsumer
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "profile_service.settings")
django.setup()

from profiles.models import MentorProfile

consumer = KafkaConsumer(
    "mentor_rating_updated",
    bootstrap_servers=[os.getenv("KAFKA_BROKER")],
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    group_id="profile_rating_group"
)

for msg in consumer:
    data = msg.value
    mentor_id = data["mentor_id"]
    avg = data["average_rating"]
    try:
        mp = MentorProfile.objects.get(id=mentor_id)
        mp.average_rating = avg
        mp.save(update_fields=["average_rating"])
        print(f"Updated mentor {mentor_id} avg rating = {avg}")
    except MentorProfile.DoesNotExist:
        print(f"MentorProfile {mentor_id} not found")
