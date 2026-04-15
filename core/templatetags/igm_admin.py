from django.contrib.admin.models import LogEntry
from django.template import Library
from django.urls import reverse

from communication.models import ContactMessage
from core.models import AcceptedDonation, ChurchHistory, CoreValue, HeroSlide, WeeklyService
from events.models import Event
from members.models import Member
from prayer.models import PrayerRequest
from sermons.models import Sermon

register = Library()

# Font Awesome 6 icon classes per "app_label.modelname" (lowercase)
MODEL_ICONS = {
    "auth.user": "fa-user-shield",
    "auth.group": "fa-users",
    "core.churchinfo": "fa-church",
    "core.corevalue": "fa-heart",
    "core.churchhistory": "fa-book-open",
    "core.heroslide": "fa-images",
    "core.weeklyservice": "fa-calendar-week",
    "core.sociallink": "fa-share-nodes",
    "core.accepteddonation": "fa-hand-holding-heart",
    "events.event": "fa-calendar-days",
    "sermons.sermon": "fa-video",
    "members.member": "fa-people-group",
    "prayer.prayerrequest": "fa-hands-praying",
    "communication.contactmessage": "fa-envelope",
}

APP_ICONS = {
    "auth": "fa-lock",
    "core": "fa-cross",
    "events": "fa-calendar-days",
    "sermons": "fa-clapperboard",
    "members": "fa-address-book",
    "prayer": "fa-dove",
    "communication": "fa-comments",
}


@register.simple_tag
def igm_model_icon(app_label, object_name):
    key = f"{app_label}.{object_name}".lower()
    return MODEL_ICONS.get(key, "fa-cube")


@register.simple_tag
def igm_app_icon(app_label):
    return APP_ICONS.get(app_label.lower(), "fa-folder")


@register.inclusion_tag("admin/igm_dashboard.html", takes_context=True)
def igm_admin_dashboard(context):
    user = context.get("user")
    admin_log = []
    if user is not None and getattr(user, "is_authenticated", False):
        admin_log = list(
            LogEntry.objects.filter(user=user).select_related("content_type")[:12]
        )
    unpublished_events = Event.objects.filter(is_published=False).count()
    unpublished_sermons = Sermon.objects.filter(is_published=False).count()
    unpublished_slides = HeroSlide.objects.filter(is_published=False).count()
    unpublished_services = WeeklyService.objects.filter(is_published=False).count()
    draft_donations = AcceptedDonation.objects.filter(is_published=False).count()
    unpublished_core = CoreValue.objects.filter(is_published=False).count()
    history_unpub = ChurchHistory.objects.filter(is_published=False).count()

    recent_events = Event.objects.order_by("-date")[:5]
    recent_sermons = Sermon.objects.order_by("-date")[:5]
    recent_messages = ContactMessage.objects.order_by("-created_at")[:5]
    recent_prayers = PrayerRequest.objects.order_by("-created_at")[:5]

    prayer_private = PrayerRequest.objects.filter(is_private=True, is_prayed=False).count()
    prayer_open = PrayerRequest.objects.filter(is_prayed=False).count()

    tiles = [
        {
            "label": "Events",
            "icon": "fa-calendar-check",
            "count": Event.objects.filter(is_published=True).count(),
            "draft": unpublished_events,
            "url": reverse("admin:events_event_changelist"),
            "add": reverse("admin:events_event_add"),
            "color": "indigo",
        },
        {
            "label": "Sermons",
            "icon": "fa-circle-play",
            "count": Sermon.objects.filter(is_published=True).count(),
            "draft": unpublished_sermons,
            "url": reverse("admin:sermons_sermon_changelist"),
            "add": reverse("admin:sermons_sermon_add"),
            "color": "sky",
        },
        {
            "label": "Members",
            "icon": "fa-users",
            "count": Member.objects.filter(is_published=True).count(),
            "draft": Member.objects.filter(is_published=False).count(),
            "url": reverse("admin:members_member_changelist"),
            "add": reverse("admin:members_member_add"),
            "color": "emerald",
        },
        {
            "label": "Prayer requests",
            "icon": "fa-hands-praying",
            "count": PrayerRequest.objects.count(),
            "extra": f"{prayer_open} open",
            "url": reverse("admin:prayer_prayerrequest_changelist"),
            "add": None,
            "color": "violet",
        },
        {
            "label": "Contact messages",
            "icon": "fa-inbox",
            "count": ContactMessage.objects.count(),
            "url": reverse("admin:communication_contactmessage_changelist"),
            "add": None,
            "color": "amber",
        },
        {
            "label": "In-kind donations",
            "icon": "fa-shirt",
            "count": AcceptedDonation.objects.filter(is_published=True).count(),
            "draft": draft_donations,
            "url": reverse("admin:core_accepteddonation_changelist"),
            "add": reverse("admin:core_accepteddonation_add"),
            "color": "rose",
        },
    ]

    content_health = (
        unpublished_events
        + unpublished_sermons
        + unpublished_slides
        + unpublished_services
        + draft_donations
        + unpublished_core
        + history_unpub
    )

    quick_links = [
        ("Church info, M-Pesa & WhatsApp", reverse("admin:core_churchinfo_changelist")),
        ("Hero slides (carousel)", reverse("admin:core_heroslide_changelist")),
        ("Weekly service times", reverse("admin:core_weeklyservice_changelist")),
        ("Social links (footer)", reverse("admin:core_sociallink_changelist")),
        ("Seminars filter", reverse("admin:events_event_changelist") + "?kind__exact=seminar_training"),
        ("Church history (About)", reverse("admin:core_churchhistory_changelist")),
        ("Django password change", reverse("admin:password_change")),
    ]

    return {
        "admin_log": admin_log,
        "tiles": tiles,
        "recent_events": recent_events,
        "recent_sermons": recent_sermons,
        "recent_messages": recent_messages,
        "recent_prayers": recent_prayers,
        "prayer_private": prayer_private,
        "content_health": content_health,
        "quick_links": quick_links,
        "unpublished_slides": unpublished_slides,
        "unpublished_services": unpublished_services,
        "app_list": context.get("app_list") or [],
        "user": context.get("user"),
        "request": context.get("request"),
    }
