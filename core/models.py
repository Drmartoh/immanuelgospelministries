from django.db import models


class ChurchInfo(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="church/logo/", blank=True, null=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    mission = models.TextField()
    vision = models.TextField()
    reverend_name = models.CharField(max_length=255, default="Rev. Samuel Muhindi Mwaura")
    reverend_bio = models.TextField(blank=True)
    reverend_photo = models.ImageField(upload_to="church/reverend/", blank=True, null=True)
    whatsapp_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Digits only, no + (e.g. 254712345678) for WhatsApp chat link.",
    )
    mpesa_paybill = models.CharField(max_length=32, blank=True, help_text="M-Pesa business / paybill number.")
    mpesa_paybill_account = models.CharField(
        max_length=64,
        blank=True,
        help_text="Account name donors should use (e.g. OFFERING).",
    )
    mpesa_till = models.CharField(max_length=32, blank=True, help_text="M-Pesa till number, if used.")

    class Meta:
        verbose_name = "Church Information"
        verbose_name_plural = "Church Information"

    def __str__(self):
        return self.name


class CoreValue(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(
        default=True,
        help_text="If unchecked, this value is hidden on the public About page.",
    )

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title


class ChurchHistory(models.Model):
    content = models.TextField()
    is_published = models.BooleanField(
        default=True,
        help_text="If unchecked, history is hidden on the public About page.",
    )

    class Meta:
        verbose_name = "Church History"
        verbose_name_plural = "Church History"

    def __str__(self):
        return "Church History"


class HeroSlide(models.Model):
    """Homepage hero carousel — image URL for easy admin without uploads."""

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image_url = models.URLField(max_length=500)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Hero slide"
        verbose_name_plural = "Hero slides"

    def __str__(self):
        return self.title


class WeeklyService(models.Model):
    """Service times shown on the home page."""

    day_label = models.CharField(max_length=64, help_text='e.g. "Wednesday"')
    name = models.CharField(max_length=200)
    time_label = models.CharField(max_length=120, help_text='e.g. "3:00 PM - 6:00 PM"')
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Weekly service time"
        verbose_name_plural = "Weekly service times"

    def __str__(self):
        return f"{self.day_label} — {self.name}"


class SocialLink(models.Model):
    label = models.CharField(max_length=64)
    url = models.URLField()
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Social link"
        verbose_name_plural = "Social links"

    def __str__(self):
        return self.label


class AcceptedDonation(models.Model):
    """In-kind gifts the church accepts from donors (managed in admin)."""

    class Category(models.TextChoices):
        CLOTHING = "clothing", "Clothing"
        FOOTWEAR = "footwear", "Shoes & footwear"
        TOYS_CHILDREN = "toys_children", "Toys for children"
        ADULTS = "adults", "Toys & gifts for adults"
        OTHER = "other", "Other in-kind gifts"

    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OTHER)
    headline = models.CharField(max_length=160)
    details = models.TextField(
        blank=True,
        help_text="Condition, sizes, drop-off instructions, or other notes for donors.",
    )
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Only published items appear on the public Giving page.",
    )

    class Meta:
        ordering = ["sort_order", "headline"]
        verbose_name = "Accepted in-kind donation"
        verbose_name_plural = "Accepted in-kind donations"

    def __str__(self):
        return self.headline
