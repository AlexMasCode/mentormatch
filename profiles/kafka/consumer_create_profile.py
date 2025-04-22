# profile_service/consumer_create_profile.py
import os, sys, json, django
from kafka import KafkaConsumer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "profile_service.settings")
django.setup()

from profiles.models import MentorProfile, MenteeProfile, Company

BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC  = os.getenv("KAFKA_TOPIC_NEW_USER", "new_user_topic")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[BROKER],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='profile_service_group',
    value_deserializer=lambda b: json.loads(b.decode())
)

print("Consumer ready")

for msg in consumer:
    data = msg.value
    user_id = data.get("user_id")
    role = data.get("role")
    company_id = data.get("company_id")
    print("EVENT:", data)

    if role == "MENTOR":
        company = None
        if company_id:
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                print("Company", company_id, "not found")

        # if the profile already existed, but the company was not set yet, we will update it
        mp, created = MentorProfile.objects.get_or_create(user_id=user_id,
                                                          defaults={"company": company})
        if not created and company and mp.company is None:
            mp.company = company
            mp.save(update_fields=["company"])
            print("Updated MentorProfile", user_id, "company →", company_id)
        elif created:
            print("Created MentorProfile", user_id, "company →", company_id)

    elif role == "MENTEE":
        MenteeProfile.objects.get_or_create(user_id=user_id)
