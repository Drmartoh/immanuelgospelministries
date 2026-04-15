from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    department = models.CharField(max_length=120)
    date_joined = models.DateField()
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="For future public directories; keep checked for active records.",
    )

    class Meta:
        ordering = ["-date_joined", "name"]

    def __str__(self):
        return f"{self.name} ({self.department})"
