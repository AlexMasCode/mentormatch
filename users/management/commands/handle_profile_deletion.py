import json
import os
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
from users.models import CustomUser


class Command(BaseCommand):
    help = "Consume profile deleted events from Kafka and delete corresponding users"

    def handle(self, *args, **options):
        kafka_broker = os.environ.get("KAFKA_BROKER", "localhost:9092")
        topic = os.environ.get("KAFKA_TOPIC_PROFILE_DELETED", "profile_deleted_topic")

        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[kafka_broker],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='auth_service_profile_deletion',
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

        self.stdout.write(self.style.SUCCESS("Auth Service Kafka consumer for profile deletion started."))

        for message in consumer:
            event = message.value
            user_id = event.get("user_id")
            if event.get("event") == "profile.deleted" and user_id:
                self.stdout.write(f"Received deletion event for user_id: {user_id}")
                try:
                    user = CustomUser.objects.get(id=user_id)
                    user.delete()
                    self.stdout.write(self.style.SUCCESS(f"Deleted user with id: {user_id}"))
                except CustomUser.DoesNotExist:
                    self.stdout.write(f"User with id {user_id} not found.")
