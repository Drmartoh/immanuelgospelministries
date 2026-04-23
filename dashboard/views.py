from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from communication.models import ContactMessage
from core.models import (
    AcceptedDonation,
    ChurchHistory,
    ChurchInfo,
    CoreValue,
    HeroSlide,
    SocialLink,
    WeeklyService,
)
from events.models import Event
from members.models import Member
from prayer.models import PrayerRequest
from sermons.models import Sermon

from .forms import (
    AcceptedDonationForm,
    ChurchHistoryForm,
    ChurchInfoForm,
    CoreValueForm,
    EventForm,
    HeroSlideForm,
    MemberForm,
    PrayerRequestNoteForm,
    SermonForm,
    SocialLinkForm,
    WeeklyServiceForm,
)


def _staff(user):
    return user.is_authenticated and user.is_staff


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not _staff(request.user):
            if request.user.is_authenticated:
                return HttpResponseForbidden("You need staff access to use this page.")
            return redirect(f"{reverse('dashboard:login')}?next={request.path}")
        return view_func(request, *args, **kwargs)

    return wrapper


class StaffAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("username", "password"):
            self.fields[name].widget.attrs.update(
                {"class": "w-full", "autocomplete": "current-password" if name == "password" else "username"}
            )
        self.fields["username"].widget.attrs["autocomplete"] = "username"


class StaffLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True
    authentication_form = StaffAuthForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(self.get_success_url())
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect("core:home")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("dashboard:home")

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(
                self.request,
                "This account does not have access to the control panel. Ask an administrator to enable staff for your user.",
            )
            return self.form_invalid(form)
        return super().form_valid(form)


@require_POST
def staff_logout(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("dashboard:login")


@staff_required
def home(request):
    stats = {
        "sermons": Sermon.objects.count(),
        "events": Event.objects.count(),
        "prayer": PrayerRequest.objects.filter(is_prayed=False).count(),
        "contact": ContactMessage.objects.count(),
    }
    return render(request, "dashboard/home.html", {"stats": stats})


@staff_required
def church_info(request):
    info = ChurchInfo.objects.first()
    if not info:
        info = ChurchInfo.objects.create(
            name="Immanuel Gospel Ministries",
            tagline="",
            description="",
            location="",
            mission="",
            vision="",
        )
    if request.method == "POST":
        form = ChurchInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, "Church information saved.")
            return redirect("dashboard:church_info")
    else:
        form = ChurchInfoForm(instance=info)
    return render(
        request,
        "dashboard/church_info.html",
        {"form": form, "section_title": "Church & contact"},
    )


@staff_required
def church_history(request):
    history = ChurchHistory.objects.order_by("id").first()
    if not history:
        history = ChurchHistory.objects.create(content="", is_published=True)
    if request.method == "POST":
        form = ChurchHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, "Church history saved.")
            return redirect("dashboard:church_history")
    else:
        form = ChurchHistoryForm(instance=history)
    return render(
        request,
        "dashboard/church_history.html",
        {"form": form, "section_title": "Church history"},
    )


# Sermons
@staff_required
def sermon_list(request):
    items = Sermon.objects.all().order_by("-date", "-id")
    return render(
        request,
        "dashboard/sermon_list.html",
        {"items": items, "section_title": "Sermons & videos"},
    )


@staff_required
def sermon_add(request):
    if request.method == "POST":
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sermon created.")
            return redirect("dashboard:sermon_list")
    else:
        form = SermonForm()
    return render(
        request,
        "dashboard/sermon_form.html",
        {
            "form": form,
            "section_title": "Add sermon",
            "is_edit": False,
        },
    )


@staff_required
def sermon_edit(request, pk):
    item = get_object_or_404(Sermon, pk=pk)
    if request.method == "POST":
        form = SermonForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Sermon updated.")
            return redirect("dashboard:sermon_list")
    else:
        form = SermonForm(instance=item)
    return render(
        request,
        "dashboard/sermon_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit sermon",
            "is_edit": True,
        },
    )


@staff_required
def sermon_delete(request, pk):
    item = get_object_or_404(Sermon, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Sermon removed.")
        return redirect("dashboard:sermon_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete sermon",
            "cancel_url": "dashboard:sermon_list",
        },
    )


# Events
@staff_required
def event_list(request):
    items = Event.objects.all().order_by("-date")
    return render(
        request,
        "dashboard/event_list.html",
        {"items": items, "section_title": "Events"},
    )


@staff_required
def event_add(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created.")
            return redirect("dashboard:event_list")
    else:
        form = EventForm()
    return render(
        request,
        "dashboard/event_form.html",
        {
            "form": form,
            "section_title": "Add event",
            "is_edit": False,
        },
    )


@staff_required
def event_edit(request, pk):
    item = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated.")
            return redirect("dashboard:event_list")
    else:
        form = EventForm(instance=item)
    return render(
        request,
        "dashboard/event_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit event",
            "is_edit": True,
        },
    )


@staff_required
def event_delete(request, pk):
    item = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Event removed.")
        return redirect("dashboard:event_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete event",
            "cancel_url": "dashboard:event_list",
        },
    )


# Hero slides
@staff_required
def hero_list(request):
    items = HeroSlide.objects.all().order_by("sort_order", "id")
    return render(
        request,
        "dashboard/hero_list.html",
        {"items": items, "section_title": "Hero slides (optional)"},
    )


@staff_required
def hero_add(request):
    if request.method == "POST":
        form = HeroSlideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Slide created.")
            return redirect("dashboard:hero_list")
    else:
        form = HeroSlideForm()
    return render(
        request,
        "dashboard/hero_form.html",
        {"form": form, "section_title": "Add hero slide", "is_edit": False},
    )


@staff_required
def hero_edit(request, pk):
    item = get_object_or_404(HeroSlide, pk=pk)
    if request.method == "POST":
        form = HeroSlideForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Slide updated.")
            return redirect("dashboard:hero_list")
    else:
        form = HeroSlideForm(instance=item)
    return render(
        request,
        "dashboard/hero_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit hero slide",
            "is_edit": True,
        },
    )


@staff_required
def hero_delete(request, pk):
    item = get_object_or_404(HeroSlide, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Slide removed.")
        return redirect("dashboard:hero_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete slide",
            "cancel_url": "dashboard:hero_list",
        },
    )


# Weekly service times
@staff_required
def weekly_list(request):
    items = WeeklyService.objects.all().order_by("sort_order", "id")
    return render(
        request,
        "dashboard/weekly_list.html",
        {"items": items, "section_title": "Weekly service times"},
    )


@staff_required
def weekly_add(request):
    if request.method == "POST":
        form = WeeklyServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Service time added.")
            return redirect("dashboard:weekly_list")
    else:
        form = WeeklyServiceForm()
    return render(
        request,
        "dashboard/weekly_form.html",
        {"form": form, "section_title": "Add service time", "is_edit": False},
    )


@staff_required
def weekly_edit(request, pk):
    item = get_object_or_404(WeeklyService, pk=pk)
    if request.method == "POST":
        form = WeeklyServiceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Service time updated.")
            return redirect("dashboard:weekly_list")
    else:
        form = WeeklyServiceForm(instance=item)
    return render(
        request,
        "dashboard/weekly_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit service time",
            "is_edit": True,
        },
    )


@staff_required
def weekly_delete(request, pk):
    item = get_object_or_404(WeeklyService, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Service time removed.")
        return redirect("dashboard:weekly_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete service time",
            "cancel_url": "dashboard:weekly_list",
        },
    )


# Social links
@staff_required
def social_list(request):
    items = SocialLink.objects.all().order_by("sort_order", "id")
    return render(
        request,
        "dashboard/social_list.html",
        {"items": items, "section_title": "Social & external links"},
    )


@staff_required
def social_add(request):
    if request.method == "POST":
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Link added.")
            return redirect("dashboard:social_list")
    else:
        form = SocialLinkForm()
    return render(
        request,
        "dashboard/social_form.html",
        {"form": form, "section_title": "Add link", "is_edit": False},
    )


@staff_required
def social_edit(request, pk):
    item = get_object_or_404(SocialLink, pk=pk)
    if request.method == "POST":
        form = SocialLinkForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Link updated.")
            return redirect("dashboard:social_list")
    else:
        form = SocialLinkForm(instance=item)
    return render(
        request,
        "dashboard/social_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit link",
            "is_edit": True,
        },
    )


@staff_required
def social_delete(request, pk):
    item = get_object_or_404(SocialLink, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Link removed.")
        return redirect("dashboard:social_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete link",
            "cancel_url": "dashboard:social_list",
        },
    )


# Core values
@staff_required
def value_list(request):
    items = CoreValue.objects.all().order_by("sort_order", "title")
    return render(
        request,
        "dashboard/value_list.html",
        {"items": items, "section_title": "Core values (About page)"},
    )


@staff_required
def value_add(request):
    if request.method == "POST":
        form = CoreValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Value added.")
            return redirect("dashboard:value_list")
    else:
        form = CoreValueForm()
    return render(
        request,
        "dashboard/value_form.html",
        {"form": form, "section_title": "Add core value", "is_edit": False},
    )


@staff_required
def value_edit(request, pk):
    item = get_object_or_404(CoreValue, pk=pk)
    if request.method == "POST":
        form = CoreValueForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Value updated.")
            return redirect("dashboard:value_list")
    else:
        form = CoreValueForm(instance=item)
    return render(
        request,
        "dashboard/value_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit core value",
            "is_edit": True,
        },
    )


@staff_required
def value_delete(request, pk):
    item = get_object_or_404(CoreValue, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Value removed.")
        return redirect("dashboard:value_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete value",
            "cancel_url": "dashboard:value_list",
        },
    )


# In-kind donations
@staff_required
def donation_list(request):
    items = AcceptedDonation.objects.all().order_by("sort_order", "headline")
    return render(
        request,
        "dashboard/donation_list.html",
        {"items": items, "section_title": "In-kind donation categories"},
    )


@staff_required
def donation_add(request):
    if request.method == "POST":
        form = AcceptedDonationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created.")
            return redirect("dashboard:donation_list")
    else:
        form = AcceptedDonationForm()
    return render(
        request,
        "dashboard/donation_form.html",
        {"form": form, "section_title": "Add category", "is_edit": False},
    )


@staff_required
def donation_edit(request, pk):
    item = get_object_or_404(AcceptedDonation, pk=pk)
    if request.method == "POST":
        form = AcceptedDonationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated.")
            return redirect("dashboard:donation_list")
    else:
        form = AcceptedDonationForm(instance=item)
    return render(
        request,
        "dashboard/donation_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit category",
            "is_edit": True,
        },
    )


@staff_required
def donation_delete(request, pk):
    item = get_object_or_404(AcceptedDonation, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Category removed.")
        return redirect("dashboard:donation_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete category",
            "cancel_url": "dashboard:donation_list",
        },
    )


# Members
@staff_required
def member_list(request):
    items = Member.objects.all().order_by("-date_joined", "name")
    return render(
        request,
        "dashboard/member_list.html",
        {"items": items, "section_title": "Members (directory)"},
    )


@staff_required
def member_add(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Member added.")
            return redirect("dashboard:member_list")
    else:
        form = MemberForm()
    return render(
        request,
        "dashboard/member_form.html",
        {"form": form, "section_title": "Add member", "is_edit": False},
    )


@staff_required
def member_edit(request, pk):
    item = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated.")
            return redirect("dashboard:member_list")
    else:
        form = MemberForm(instance=item)
    return render(
        request,
        "dashboard/member_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Edit member",
            "is_edit": True,
        },
    )


@staff_required
def member_delete(request, pk):
    item = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Member removed.")
        return redirect("dashboard:member_list")
    return render(
        request,
        "dashboard/confirm_delete.html",
        {
            "object": item,
            "section_title": "Delete member",
            "cancel_url": "dashboard:member_list",
        },
    )


# Prayer requests
@staff_required
def prayer_list(request):
    items = PrayerRequest.objects.all().order_by("-created_at")
    return render(
        request,
        "dashboard/prayer_list.html",
        {"items": items, "section_title": "Prayer requests"},
    )


@staff_required
def prayer_edit(request, pk):
    item = get_object_or_404(PrayerRequest, pk=pk)
    if request.method == "POST":
        form = PrayerRequestNoteForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Request updated.")
            return redirect("dashboard:prayer_list")
    else:
        form = PrayerRequestNoteForm(instance=item)
    return render(
        request,
        "dashboard/prayer_form.html",
        {
            "form": form,
            "item": item,
            "section_title": "Prayer request",
        },
    )


# Contact messages
@staff_required
def message_list(request):
    items = ContactMessage.objects.all().order_by("-created_at")
    return render(
        request,
        "dashboard/message_list.html",
        {"items": items, "section_title": "Contact messages"},
    )


@staff_required
def message_detail(request, pk):
    item = get_object_or_404(ContactMessage, pk=pk)
    return render(
        request,
        "dashboard/message_detail.html",
        {"item": item, "section_title": "Message"},
    )
