from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [

    path('', views.index, name='index'),

    path('locations/', views.locations, name='locations'),
    path('location/<int:location_id>/', views.location, name='location'),

    path('routes/', views.routes, name='routes'),
    path('route_map/<int:route_id>/', views.route_map, name='route_map'),
    path('route_storymap/<int:route_id>/', views.route_storymap, name='route_storymap'),

    path('map_closed_lines_select/', views.map_closed_lines_select, name='map_closed_lines_select'),
    path('map_closed_lines/<str:county_name>/', views.MapClosedLines.as_view(), name='map_closed_lines'),

    path('elrs/', views.elrs, name='elrs'),
    path('elr_map/<int:elr_id>/', views.elr_map, name='elr_map'),
    path('elr_storymap/<int:elr_id>/', views.elr_storymap, name='elr_storymap'),

    path('osm_railmap_county_select/', views.osm_railmap_county_select, name='osm_railmap_county_select'),
    path('osm_railmap_county/<str:county>/', views.osm_railmap_county, name='osm_railmap_county'),

    path('trackmap/', views.Trackmap.as_view(), name='trackmap'),

    path('location_timeline/', views.location_timeline, name='location_timeline'),

    path('depots_vis_timeline/', views.depot_vis_timeline, name='depot_vis_timeline'),
    ]