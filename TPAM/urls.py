from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
  path('admin/', admin.site.urls),
  path('tinymce/', include('tinymce.urls')),
  path('chaining/', include('smart_selects.urls')),

  re_path(r'', include('mainmenu.urls', namespace="mainmenu")),
  re_path(r'^api/', include('api.urls', namespace="api")),
  re_path(r'^users/', include('users.urls', namespace="users")),
  re_path(r'^rtt/', include('rtt.urls', namespace="rtt")),
  re_path(r'^locos/', include('locos.urls', namespace="locos")),
  re_path(r'^mvs/', include('mvs.urls', namespace="mvs")),
  re_path(r'^aircraft/', include('aircraft.urls', namespace="aircraft")),
  re_path(r'^maps/', include('maps.urls', namespace="maps")),
  re_path(r'^vehicles/', include('vehicles.urls', namespace="vehicles")),
  re_path(r'^storymaps/', include('storymaps.urls', namespace="storymaps")),
  re_path(r'^locations/', include('locations.urls', namespace="locations")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
    SHOW_TOOLBAR_CALLBACK = True