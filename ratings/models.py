from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class MentorReview(models.Model):
    session = models.OneToOneField(
        "session_app.Session",
        on_delete=models.CASCADE,
        related_name="mentor_review"
    )
    mentor_id = models.IntegerField()
    mentee_id = models.IntegerField()
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mentor_id"]),
        ]

class MenteeRating(models.Model):
    session = models.OneToOneField(
        "session_app.Session",
        on_delete=models.CASCADE,
        related_name="mentee_rating"
    )
    mentor_id = models.IntegerField()
    mentee_id = models.IntegerField()
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    feedback = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mentee_id"]),
        ]
