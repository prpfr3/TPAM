from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from TPAM.admin import CustomAdminSite

admin.site.__class__ = CustomAdminSite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("chaining/", include("smart_selects.urls")),
    path("", include("mainmenu.urls", namespace="mainmenu")),
    path("api/", include("api.urls", namespace="api")),
    path("users/", include("users.urls", namespace="users")),
    path("rtt/", include("rtt.urls", namespace="rtt")),
    path("locos/", include("locos.urls", namespace="locos")),
    path("companies/", include("companies.urls", namespace="companies")),
    path("mvs/", include("mvs.urls", namespace="mvs")),
    path("aircraft/", include("aircraft.urls", namespace="aircraft")),
    path("notes/", include("notes.urls", namespace="notes")),
    path("people/", include("people.urls", namespace="people")),
    path("vehicles/", include("vehicles.urls", namespace="vehicles")),
    path("storymaps/", include("storymaps.urls", namespace="storymaps")),
    path("locations/", include("locations.urls", namespace="locations")),
    path("timelines/", include("timelines.urls", namespace="timelines")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    SHOW_TOOLBAR_CALLBACK = True
