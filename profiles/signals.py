from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import MentorProfile, MenteeProfile
from .kafka.producer_delete_profile import publish_profile_deleted_event

@receiver(post_delete, sender=MentorProfile)
def mentor_profile_deleted(sender, instance, **kwargs):
    publish_profile_deleted_event(instance.user_id)

@receiver(post_delete, sender=MenteeProfile)
def mentee_profile_deleted(sender, instance, **kwargs):
    publish_profile_deleted_event(instance.user_id)
