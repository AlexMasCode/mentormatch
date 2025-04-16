import os
import json
from kafka import KafkaProducer

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC_NEW_USER = os.environ.get("KAFKA_TOPIC_NEW_USER", "new_user_topic")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_new_user_event(user, company_id=None):
    """
    Publishes an event for new user registration.
    The required fields are: user_id, email, first_name, last_name, and role.
    If company_id is provided (for mentors), it's added to the payload.
    """
    event = {
        "user_id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
    }

    if company_id is not None:
        event["company_id"] = company_id

    producer.send(TOPIC_NEW_USER, event)
    producer.flush()

    print(f"Published new user event: {event}")
