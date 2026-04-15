from django.contrib import admin

from .models import (
    AcceptedDonation,
    ChurchHistory,
    ChurchInfo,
    CoreValue,
    HeroSlide,
    SocialLink,
    WeeklyService,
)


def _ordered_app_list(request, app_label=None):
    app_order = {
        "core": 1,
        "events": 2,
        "sermons": 3,
        "members": 4,
        "prayer": 5,
        "communication": 6,
        "auth": 7,
    }
    app_list = admin.AdminSite.get_app_list(admin.site, request, app_label)
    app_list.sort(key=lambda app: app_order.get(app["app_label"], 99))
    for app in app_list:
        app["models"].sort(key=lambda m: m["name"])
    return app_list


admin.site.get_app_list = _ordered_app_list
admin.site.site_header = "Immanuel Gospel Ministries — Admin"
admin.site.site_title = "IGM Dashboard"
admin.site.index_title = "Site overview & apps"


@admin.register(ChurchInfo)
class ChurchInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "reverend_name", "mpesa_paybill", "mpesa_till")
    fieldsets = (
        ("Church identity", {"fields": ("name", "tagline", "logo", "description", "location")}),
        ("Leadership", {"fields": ("reverend_name", "reverend_bio", "reverend_photo")}),
        ("Direction", {"fields": ("mission", "vision")}),
        ("Contact & social", {"fields": ("whatsapp_phone",)}),
        ("M-Pesa (shown on Giving page)", {"fields": ("mpesa_paybill", "mpesa_paybill_account", "mpesa_till")}),
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_published")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")
    search_fields = ("title", "description")


@admin.register(ChurchHistory)
class ChurchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "is_published", "preview")
    list_filter = ("is_published",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj.content:
            return "—"
        return (obj.content[:80] + "…") if len(obj.content) > 80 else obj.content


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_published", "image_url")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")
    search_fields = ("title", "subtitle")


@admin.register(WeeklyService)
class WeeklyServiceAdmin(admin.ModelAdmin):
    list_display = ("day_label", "name", "time_label", "sort_order", "is_published")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")
    search_fields = ("name", "day_label")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "sort_order", "is_published")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")


@admin.register(AcceptedDonation)
class AcceptedDonationAdmin(admin.ModelAdmin):
    list_display = ("headline", "category", "sort_order", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("headline", "details")
    list_editable = ("sort_order", "is_published")
