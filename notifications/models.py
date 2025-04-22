from django.db import models

class Notification(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user_id']),]
        ordering = ['-created_at']