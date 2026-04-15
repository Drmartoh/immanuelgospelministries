from django import forms
from .models import PrayerRequest


class PrayerRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "is_private":
                field.widget.attrs["class"] = "input-checkbox"
            else:
                field.widget.attrs["class"] = "form-control"

    class Meta:
        model = PrayerRequest
        fields = ["name", "request", "is_private"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name (optional)"}),
            "request": forms.Textarea(attrs={"rows": 5, "placeholder": "Share your prayer request"}),
        }
