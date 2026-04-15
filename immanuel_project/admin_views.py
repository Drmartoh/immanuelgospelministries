"""Custom admin pages (same auth and context as Django admin)."""

from django.contrib import admin
from django.template.response import TemplateResponse


def admin_control_center(request):
    """
    Full control centre at /admin/dashboard/ — same data as the admin index
    (app list, log entries context, permissions) without redirecting elsewhere.
    """
    request.current_app = admin.site.name
    context = {
        **admin.site.each_context(request),
        "title": admin.site.index_title,
        "subtitle": None,
        "app_list": admin.site.get_app_list(request),
    }
    return TemplateResponse(request, "admin/dashboard.html", context)
