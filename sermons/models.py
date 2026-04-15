from django.db import models
from urllib.parse import parse_qs, urlparse


class Sermon(models.Model):
    title = models.CharField(max_length=255)
    preacher = models.CharField(max_length=255)
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to="sermons/audio/", blank=True, null=True)
    date = models.DateField()
    thumbnail = models.ImageField(upload_to="sermons/thumbnails/", blank=True, null=True)
    is_published = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck to hide this sermon from the public website (draft).",
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.title} ({self.preacher})"

    @property
    def embed_video_url(self):
        if not self.video_url:
            return ""
        parsed = urlparse(self.video_url)
        host = parsed.netloc.lower()
        path = parsed.path.strip("/")

        # Supports youtube.com/watch?v=ID, youtu.be/ID, shorts/ID and embed/ID
        if "youtu.be" in host and path:
            return f"https://www.youtube.com/embed/{path.split('/')[0]}"
        if "youtube.com" in host:
            if path == "watch":
                video_id = parse_qs(parsed.query).get("v", [""])[0]
                if video_id:
                    return f"https://www.youtube.com/embed/{video_id}"
            if path.startswith("embed/"):
                return f"https://www.youtube.com/{path}"
            if path.startswith("shorts/"):
                video_id = path.split("/", 1)[1]
                return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=900&q=80"
