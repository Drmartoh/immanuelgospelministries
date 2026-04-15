from django.db import models


class PrayerRequest(models.Model):
    name = models.CharField(max_length=255, blank=True)
    request = models.TextField()
    is_private = models.BooleanField(default=False)
    is_prayed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        label = self.name if self.name else "Anonymous"
        return f"{label} - {self.created_at:%Y-%m-%d}"
