from django.contrib import admin
from .models import PrayerRequest


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "is_private", "is_prayed", "created_at")
    list_filter = ("is_private", "is_prayed", "created_at")
    search_fields = ("name", "request")
    date_hierarchy = "created_at"
