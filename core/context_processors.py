from .models import ChurchInfo, SocialLink


def site_context(request):
    return {
        "church_info": ChurchInfo.objects.first(),
        "social_links": SocialLink.objects.filter(is_published=True).order_by("sort_order", "id"),
    }
