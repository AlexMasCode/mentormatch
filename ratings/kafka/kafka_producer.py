# ratings/kafka/kafka_producer.py
import json
import logging
from kafka import KafkaProducer
from django.conf import settings

logger = logging.getLogger(__name__)

def get_producer():
    """
    Creates and returns a KafkaProducer instance.
    This function is used to avoid connecting to Kafka at the time of module import.
    """
    return KafkaProducer(
        bootstrap_servers=[settings.KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

def send_rating_update(mentor_id: int, average_rating: float):
    """
    Sends an updated average rating for a mentor to the profile service via Kafka.
    """
    try:
        producer = get_producer()
        payload = {
            "mentor_id": mentor_id,
            "average_rating": average_rating,
        }
        producer.send(settings.KAFKA_TOPIC_RATING_UPDATE, payload)
        producer.flush()
        logger.debug(f"Sent rating update to Kafka: {payload}")
    except Exception as e:
        logger.error(f"Failed to send rating update: {e}")
