# notifications/kafka_consumer.py
import os, django, json, threading
from kafka import KafkaConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service.settings')
django.setup()

from notifications.models import Notification
from django.conf import settings

consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=[settings.KAFKA_BROKER],
    group_id=os.getenv('GROUP_ID', 'notification-group'),
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=False
)

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=int(os.getenv('WORKER_THREADS', '5')))


def handle_message(msg):
    data = msg.value
    # expected payload: {"user_id":..., "message":...}
    Notification.objects.create(
        user_id=data['user_id'],
        message=data['message']
    )


def consume_loop():
    while True:
        records = consumer.poll(timeout_ms=1000, max_records=20)
        for tp, msgs in records.items():
            for msg in msgs:
                executor.submit(handle_message, msg)
        consumer.commit()


if __name__ == '__main__':
    consume_loop()