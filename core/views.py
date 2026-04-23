from django.db.models import Q
from django.shortcuts import render
from django.templatetags.static import static
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
    return [
        {
            "title": "Rev. Samuel Muhindi Mwaura",
            "subtitle": "Senior Pastor, Immanuel Gospel Ministries",
            "image": static("images/hero/pastor-muhindi-profile.png"),
        },
        {
            "title": "Worship and Fellowship",
            "subtitle": "Moments of faith, prayer, and praise in our church family.",
            "image": static("images/gallery/pastor-study-1.png"),
        },
        {
            "title": "Church Leadership",
            "subtitle": "Serving with love, integrity, and biblical teaching.",
            "image": static("images/gallery/pastor-seated-1.png"),
        },
        {
            "title": "Family and Community",
            "subtitle": "Building stronger homes and relationships through Christ.",
            "image": static("images/gallery/pastor-couple-1.png"),
        },
        {
            "title": "Together in Ministry",
            "subtitle": "Walking in faith and sharing God’s love with others.",
            "image": static("images/gallery/pastor-couple-2.png"),
        },
        {
            "title": "Joyful Fellowship",
            "subtitle": "Celebrating the goodness of God in every season.",
            "image": static("images/gallery/pastor-couple-3.png"),
        },
        {
            "title": "Ministry Highlights",
            "subtitle": "Recent moments from church services and outreach.",
            "image": static("images/gallery/facebook-gallery-1.jpg"),
        },
        {
            "title": "Sunday Gatherings",
            "subtitle": "Worship, the Word, and fellowship with one heart.",
            "image": static("images/gallery/facebook-gallery-2.jpg"),
        },
        {
            "title": "Faith in Action",
            "subtitle": "Growing in prayer, discipleship, and service.",
            "image": static("images/gallery/facebook-gallery-3.jpg"),
        },
        {
            "title": "Church Moments",
            "subtitle": "Snapshots of God’s grace in our congregation.",
            "image": static("images/gallery/facebook-gallery-4.jpg"),
        },
        {
            "title": "Community Life",
            "subtitle": "A welcoming home for worship and spiritual growth.",
            "image": static("images/gallery/facebook-gallery-5.jpg"),
        },
        {
            "title": "Immanuel Gospel Ministries",
            "subtitle": "Serving God and touching lives through the Gospel.",
            "image": static("images/gallery/facebook-gallery-6.jpg"),
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
    videos_qs = pub_sermons.exclude(video_url="").order_by("-date")
    featured_video = videos_qs.first()
    featured_videos = videos_qs[1:5] if featured_video else videos_qs[:4]
    gallery_items = [
        item
        for item in list(latest_events[:4]) + list(latest_sermons[:4])
        if getattr(item, "image", None) or getattr(item, "thumbnail", None)
    ]
    static_gallery_items = [
        {"image_url": static("images/gallery/pastor-study-1.png"), "alt": "Pastor Muhindi studying scripture"},
        {"image_url": static("images/gallery/pastor-seated-1.png"), "alt": "Pastor Muhindi at church service"},
        {"image_url": static("images/gallery/pastor-couple-1.png"), "alt": "Pastor Muhindi with family"},
        {"image_url": static("images/gallery/pastor-couple-2.png"), "alt": "Pastor Muhindi with family outdoors"},
        {"image_url": static("images/gallery/pastor-couple-3.png"), "alt": "Pastor Muhindi with family portrait"},
        {"image_url": static("images/gallery/facebook-gallery-1.jpg"), "alt": "Immanuel Gospel Ministries gallery image 1"},
        {"image_url": static("images/gallery/facebook-gallery-2.jpg"), "alt": "Immanuel Gospel Ministries gallery image 2"},
        {"image_url": static("images/gallery/facebook-gallery-3.jpg"), "alt": "Immanuel Gospel Ministries gallery image 3"},
        {"image_url": static("images/gallery/facebook-gallery-4.jpg"), "alt": "Immanuel Gospel Ministries gallery image 4"},
        {"image_url": static("images/gallery/facebook-gallery-5.jpg"), "alt": "Immanuel Gospel Ministries gallery image 5"},
        {"image_url": static("images/gallery/facebook-gallery-6.jpg"), "alt": "Immanuel Gospel Ministries gallery image 6"},
    ]
    gallery_items = [*static_gallery_items, *gallery_items]

    context = {
        "info": ChurchInfo.objects.first(),
        "upcoming_events": upcoming[:4],
        "latest_events": latest_events,
        "latest_sermons": latest_sermons,
        "seminars": seminars,
        "featured_videos": featured_videos,
        "featured_video": featured_video,
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
