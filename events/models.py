from django.db import models


class Event(models.Model):
    class Kind(models.TextChoices):
        GENERAL = "general", "General / fellowship / outreach"
        SEMINAR_TRAINING = "seminar_training", "Seminar & skills training (entrepreneurship, empowerment, etc.)"

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events/", blank=True, null=True)
    kind = models.CharField(
        max_length=32,
        choices=Kind.choices,
        default=Kind.GENERAL,
        db_index=True,
        help_text="Use “Seminar & skills training” for entrepreneurship, empowerment, and similar programs.",
    )
    training_focus = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short label, e.g. Entrepreneurship, Financial literacy, Youth empowerment.",
    )
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck to hide this event from the public website (draft).",
    )

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.title} - {self.date:%Y-%m-%d}"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=900&q=80"
