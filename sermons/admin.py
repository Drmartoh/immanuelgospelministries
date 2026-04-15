from django.contrib import admin
from .models import Sermon


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ("title", "preacher", "date", "is_published")
    search_fields = ("title", "preacher")
    list_filter = ("date", "preacher", "is_published")
    list_editable = ("is_published",)
    date_hierarchy = "date"
    list_per_page = 25
