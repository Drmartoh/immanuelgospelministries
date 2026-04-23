from django import forms

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


class ChurchInfoForm(forms.ModelForm):
    class Meta:
        model = ChurchInfo
        fields = [
            "name",
            "tagline",
            "logo",
            "description",
            "location",
            "mission",
            "vision",
            "reverend_name",
            "reverend_bio",
            "reverend_photo",
            "whatsapp_phone",
            "mpesa_paybill",
            "mpesa_paybill_account",
            "mpesa_till",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "mission": forms.Textarea(attrs={"rows": 3}),
            "vision": forms.Textarea(attrs={"rows": 3}),
            "reverend_bio": forms.Textarea(attrs={"rows": 4}),
            "whatsapp_phone": forms.TextInput(
                attrs={"placeholder": "254712345678 (digits only, no +)"}
            ),
        }


class ChurchHistoryForm(forms.ModelForm):
    class Meta:
        model = ChurchHistory
        fields = ["content", "is_published"]
        widgets = {"content": forms.Textarea(attrs={"rows": 12})}


class CoreValueForm(forms.ModelForm):
    class Meta:
        model = CoreValue
        fields = ["title", "description", "sort_order", "is_published"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = ["title", "subtitle", "image_url", "sort_order", "is_published"]
        widgets = {"subtitle": forms.Textarea(attrs={"rows": 2})}


class WeeklyServiceForm(forms.ModelForm):
    class Meta:
        model = WeeklyService
        fields = ["day_label", "name", "time_label", "sort_order", "is_published"]


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["label", "url", "sort_order", "is_published"]


class AcceptedDonationForm(forms.ModelForm):
    class Meta:
        model = AcceptedDonation
        fields = ["category", "headline", "details", "sort_order", "is_published"]
        widgets = {"details": forms.Textarea(attrs={"rows": 3})}


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = [
            "title",
            "preacher",
            "video_url",
            "audio_file",
            "date",
            "thumbnail",
            "is_published",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "video_url": forms.URLInput(
                attrs={"placeholder": "https://youtu.be/... or YouTube link"}
            ),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "location",
            "image",
            "kind",
            "training_focus",
            "is_published",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget = forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local", "class": "w-full max-w-md"},
        )
        self.fields["date"].input_formats = [
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%dT%H:%M:%S",
        ]
        if self.instance and self.instance.pk and self.instance.date:
            d = self.instance.date
            if hasattr(d, "astimezone"):
                from django.utils import timezone

                if timezone.is_aware(d):
                    d = timezone.localtime(d)
            self.initial["date"] = d.strftime("%Y-%m-%dT%H:%M")


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "name",
            "phone",
            "email",
            "department",
            "date_joined",
            "is_published",
        ]
        widgets = {"date_joined": forms.DateInput(attrs={"type": "date"})}


class PrayerRequestNoteForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ["is_prayed", "is_private"]


# ContactMessage is read-only in UI; no form for create from dashboard
