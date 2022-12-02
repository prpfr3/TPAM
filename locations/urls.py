from django.urls import include, path, re_path
from . import views

app_name = 'locations'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),

    re_path(r'^locations/$', views.locations, name='locations'),
    re_path(r'^location/(?P<location_id>\d+)/$', views.location, name='location'),

    re_path(r'^routes/$', views.routes, name='routes'),
    re_path(r'^routemap_storymap/(?P<route_id>\d+)/$', views.routemap_storymap, name='routemap_storymap'),
    re_path(r'^routemap/(?P<route_id>\d+)/$', views.routemap, name='routemap'),

    re_path(r'^map_closed_lines_select/$', views.map_closed_lines_select, name='map_closed_lines_select'),
    re_path(r'^map_closed_lines/(?P<county_name>[^/]+)/$', views.MapClosedLines.as_view(), name='map_closed_lines'),

    re_path(r'^osm_rail_map_select/$', views.osm_rail_map_select, name='osm_rail_map_select'),
    re_path(r'^osm_rail_map/(?P<elr_id>\d+)/$', views.osm_rail_map, name='osm_rail_map'),

    re_path(r'^trackmap/$', views.Trackmap.as_view(), name='trackmap'),

    re_path(r'^location_timeline/$', views.location_timeline, name='location_timeline'),

    re_path(r'^depots_vis_timeline/$', views.depot_vis_timeline, name='depot_vis_timeline'),
    ]