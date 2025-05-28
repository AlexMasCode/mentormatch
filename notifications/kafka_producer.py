import os
import json
from kafka import KafkaProducer

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_NOTIFICATIONS", "notifications")


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    retries=5
)

def send_user_notification(user_id: int, message: str):

    payload = {
        "user_id": user_id,
        "message": message
    }
    producer.send(KAFKA_TOPIC, payload)
    producer.flush()
