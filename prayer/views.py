from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import PrayerRequestForm


def prayer_request(request):
    form = PrayerRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your prayer request has been submitted.")
        return redirect("prayer:request")
    return render(request, "prayer/request.html", {"form": form})
