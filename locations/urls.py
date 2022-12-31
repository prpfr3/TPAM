from django.urls import include, path, re_path
from . import views

app_name = 'locations'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),

    re_path(r'^locations/$', views.locations, name='locations'),
    re_path(r'^location/(?P<location_id>\d+)/$', views.location, name='location'),

    re_path(r'^routes/$', views.routes, name='routes'),
    re_path(r'^route_map/(?P<route_id>\d+)/$', views.route_map, name='route_map'),
    re_path(r'^route_storymap/(?P<route_id>\d+)/$', views.route_storymap, name='route_storymap'),

    re_path(r'^map_closed_lines_select/$', views.map_closed_lines_select, name='map_closed_lines_select'),
    re_path(r'^map_closed_lines/(?P<county_name>[^/]+)/$', views.MapClosedLines.as_view(), name='map_closed_lines'),

    re_path(r'^elrs/$', views.elrs, name='elrs'),
    re_path(r'^elr_map/(?P<elr_id>\d+)/$', views.elr_map, name='elr_map'),
    re_path(r'^elr_storymap/(?P<elr_id>\d+)/$', views.elr_storymap, name='elr_storymap'),

    re_path(r'^osm_railmap_county_select/$', views.osm_railmap_county_select, name='osm_railmap_county_select'),
    re_path(r'^osm_railmap_county/(?P<county>[^/]+)/$', views.osm_railmap_county, name='osm_railmap_county'),

    re_path(r'^trackmap/$', views.Trackmap.as_view(), name='trackmap'),

    re_path(r'^location_timeline/$', views.location_timeline, name='location_timeline'),

    re_path(r'^depots_vis_timeline/$', views.depot_vis_timeline, name='depot_vis_timeline'),
    ]