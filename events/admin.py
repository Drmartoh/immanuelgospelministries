from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "is_published", "training_focus", "date", "location")
    search_fields = ("title", "description", "location", "training_focus")
    list_filter = ("kind", "is_published", "date")
    list_editable = ("is_published",)
    date_hierarchy = "date"
    list_per_page = 25
    fieldsets = (
        (None, {"fields": ("title", "description", "date", "location", "image", "is_published")}),
        ("Seminars & training", {"fields": ("kind", "training_focus")}),
    )
