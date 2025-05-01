# profiles/producer_delete_profile.py
import os
import json
from kafka import KafkaProducer


KAFKA_BROKER = os.environ.get("KAFKA_BROKER")
TOPIC_PROFILE_DELETED = os.environ.get("KAFKA_TOPIC_PROFILE_DELETED")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_profile_deleted_event(user_id):
    event = {
        "user_id": user_id,
        "event": "profile.deleted"
    }
    producer.send(TOPIC_PROFILE_DELETED, event)
    producer.flush()
    print(f"Published profile deleted event: {event}")

# If the profile creation function already exists, it will remain unchanged:
def publish_new_user_event(user):
    event = {
        "user_id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
    }
    producer.send(os.environ.get("KAFKA_TOPIC_NEW_USER", "new_user_topic"), event)
    producer.flush()
    print(f"Published new user event: {event}")
