from django.db import models

class Availability(models.Model):
    mentor_id = models.IntegerField(
        help_text="Mentor ID from Profile Service"
    )
    start_ts = models.DateTimeField(
        help_text="Start of the availability interval"
    )
    end_ts = models.DateTimeField(
        help_text="End of the availability interval"
    )
    is_recurring = models.BooleanField(
        default=False,
        help_text="Recurring availability (e.g., weekly)"
    )

    is_booked = models.BooleanField(
        default=False,
        help_text="True if this slot has already been booked"
    )

    class Meta:
        ordering = ['start_ts']
        indexes = [
            models.Index(fields=['mentor_id', 'start_ts']),
            models.Index(fields=['mentor_id', 'is_booked']),
        ]

    def __str__(self):
        return f"Mentor {self.mentor_id}: {self.start_ts} → {self.end_ts}"


class Session(models.Model):
    STATUS_PENDING   = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_DECLINED  = 'declined'
    STATUS_CHOICES = [
        (STATUS_PENDING,   'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_DECLINED,  'Declined'),
    ]

    mentor_id = models.IntegerField(
        help_text="Mentor ID from Profile Service"
    )
    mentee_id = models.IntegerField(
        help_text="Mentee ID from Profile Service"
    )
    start_ts = models.DateTimeField(
        help_text="Session start time"
    )
    end_ts = models.DateTimeField(
        help_text="Session end time"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text="Booking status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_ts']
        indexes = [
            models.Index(fields=['mentor_id', 'start_ts']),
            models.Index(fields=['mentee_id', 'status']),
        ]

    def __str__(self):
        return f"Session {self.id}: {self.mentor_id} ↔ {self.mentee_id} [{self.status}]"
