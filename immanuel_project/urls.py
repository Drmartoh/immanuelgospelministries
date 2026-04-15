from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from immanuel_project.admin_views import admin_control_center

urlpatterns = [
    path(
        "admin/dashboard/",
        admin.site.admin_view(admin_control_center),
        name="admin_dashboard",
    ),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("events/", include("events.urls")),
    path("sermons/", include("sermons.urls")),
    path("prayer/", include("prayer.urls")),
    path("", include("communication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
