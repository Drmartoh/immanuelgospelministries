from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from events.models import Event
from sermons.models import Sermon

from .models import (
    AcceptedDonation,
    ChurchHistory,
    ChurchInfo,
    CoreValue,
    HeroSlide,
    WeeklyService,
)


def _carousel_slides():
    slides = list(
        HeroSlide.objects.filter(is_published=True).order_by("sort_order", "id").values(
            "title", "subtitle", "image_url"
        )
    )
    if slides:
        return [{"title": s["title"], "subtitle": s["subtitle"], "image": s["image_url"]} for s in slides]
    return [
        {
            "title": "Welcome to Immanuel Gospel Ministries",
            "subtitle": "Growing in faith, prayer, and God's Word together.",
            "image": "https://images.unsplash.com/photo-1438232992991-995b7058bbb3?auto=format&fit=crop&w=1600&q=80",
        },
        {
            "title": "Join Us Every Sunday",
            "subtitle": "Bible study, praise and worship, main service, and deliverance prayers.",
            "image": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1600&q=80",
        },
        {
            "title": "Midweek Biblical Studies",
            "subtitle": "Wednesday fellowship dedicated to prayer and scripture.",
            "image": "https://images.unsplash.com/photo-1504052434569-70ad5836ab65?auto=format&fit=crop&w=1600&q=80",
        },
    ]


def _service_times():
    rows = WeeklyService.objects.filter(is_published=True).order_by("sort_order", "id")
    if rows.exists():
        return [{"day": r.day_label, "name": r.name, "time": r.time_label} for r in rows]
    return [
        {"day": "Wednesday", "time": "3:00 PM - 6:00 PM", "name": "Biblical Studies and Prayers"},
        {"day": "Sunday", "time": "10:00 AM - 11:00 AM", "name": "Bible Study"},
        {"day": "Sunday", "time": "11:00 AM - 12:00 PM", "name": "Praise and Worship"},
        {
            "day": "Sunday",
            "time": "12:00 PM - 1:30 PM",
            "name": "Main Service and Deliverance Prayers",
        },
    ]


def home(request):
    now = timezone.now()
    pub_events = Event.objects.filter(is_published=True)
    pub_sermons = Sermon.objects.filter(is_published=True)

    upcoming = pub_events.filter(date__gte=now).order_by("date")
    latest_events = pub_events.order_by("-date")[:6]
    latest_sermons = pub_sermons.order_by("-date")[:6]
    seminars = (
        pub_events.filter(Q(kind=Event.Kind.SEMINAR_TRAINING) | Q(title__icontains="seminar"))
        .distinct()
        .order_by("date")[:6]
    )
    featured_videos = pub_sermons.exclude(video_url="").order_by("-date")[:6]
    gallery_items = [
        item
        for item in list(latest_events[:4]) + list(latest_sermons[:4])
        if getattr(item, "image", None) or getattr(item, "thumbnail", None)
    ]

    context = {
        "info": ChurchInfo.objects.first(),
        "upcoming_events": upcoming[:4],
        "latest_events": latest_events,
        "latest_sermons": latest_sermons,
        "seminars": seminars,
        "featured_videos": featured_videos,
        "gallery_items": gallery_items,
        "carousel_slides": _carousel_slides(),
        "service_times": _service_times(),
    }
    return render(request, "core/home.html", context)


def about(request):
    history = ChurchHistory.objects.filter(is_published=True).order_by("id").first()
    context = {
        "info": ChurchInfo.objects.first(),
        "history": history,
        "values": CoreValue.objects.filter(is_published=True).order_by("sort_order", "title"),
    }
    return render(request, "core/about.html", context)


def services(request):
    weekly_services = [
        {
            "title": "Wednesday Fellowship",
            "time": "Wednesday 3:00 PM - 6:00 PM",
            "description": "Biblical Studies and Prayers",
        },
        {
            "title": "Sunday Bible Study",
            "time": "Sunday 10:00 AM - 11:00 AM",
            "description": "Interactive scripture teaching.",
        },
        {
            "title": "Sunday Praise and Worship",
            "time": "Sunday 11:00 AM - 12:00 PM",
            "description": "Worship and thanksgiving with the congregation.",
        },
        {
            "title": "Main Service",
            "time": "Sunday 12:00 PM - 1:30 PM",
            "description": "Word ministry and deliverance prayers.",
        },
    ]
    return render(request, "core/services.html", {"weekly_services": weekly_services})


def giving(request):
    donations = AcceptedDonation.objects.filter(is_published=True).order_by("sort_order", "headline")
    return render(
        request,
        "core/giving.html",
        {
            "accepted_donations": donations,
        },
    )
