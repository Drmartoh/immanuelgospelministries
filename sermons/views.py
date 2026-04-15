from django.shortcuts import render

from .models import Sermon


def sermon_list(request):
    sermons = Sermon.objects.filter(is_published=True).order_by("-date")
    return render(request, "sermons/list.html", {"sermons": sermons})
