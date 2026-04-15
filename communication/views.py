from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactMessageForm


def contact(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thank you for contacting us. We will reach out soon.")
        return redirect("communication:contact")
    return render(request, "communication/contact.html", {"form": form})
