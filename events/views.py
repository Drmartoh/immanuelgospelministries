from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Event


def event_list(request):
    events = Event.objects.filter(is_published=True).order_by("date")
    return render(request, "events/list.html", {"events": events})


def seminar_list(request):
    seminars = (
        Event.objects.filter(is_published=True)
        .filter(Q(kind=Event.Kind.SEMINAR_TRAINING) | Q(title__icontains="seminar"))
        .distinct()
        .order_by("date")
    )
    return render(request, "events/seminars.html", {"seminars": seminars})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, is_published=True)
    return render(request, "events/detail.html", {"event": event})
