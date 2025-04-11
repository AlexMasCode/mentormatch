# auth_service/users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .kafka_producer import publish_new_user_event

@receiver(post_save, sender=CustomUser)
def send_new_user_event(sender, instance, created, **kwargs):
    if created:
        publish_new_user_event(instance)
