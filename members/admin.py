from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "is_published", "phone", "email", "date_joined")
    search_fields = ("name", "department", "email")
    list_filter = ("department", "is_published", "date_joined")
    list_editable = ("is_published",)
    date_hierarchy = "date_joined"
