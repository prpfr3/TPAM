from django.urls import path
from . import views, views_wip

app_name = 'locations'

urlpatterns = [

    path('', views.index, name='index'),

    path('locations/', views.locations, name='locations'),
    path('location/<int:location_id>/', views.location, name='location'),

    path('routes/', views.routes, name='routes'),
    path('route/<int:route_id>/', views.route, name='route'),
    path('route_storymap/<int:route_id>/', views.route_storymap, name='route_storymap'),

    path('map_closed_lines_select/', views_wip.map_closed_lines_select, name='map_closed_lines_select'),
    path('map_closed_lines/<str:county_name>/', views_wip.MapClosedLines.as_view(), name='map_closed_lines'),

    path('elrs/', views.elrs, name='elrs'),
    path('elr_map/<int:elr_id>/', views.elr_map, name='elr_map'),
    path('elr_storymap/<int:elr_id>/', views.elr_storymap, name='elr_storymap'),

    path('osm_railmap_county_select/', views.osm_railmap_county_select, name='osm_railmap_county_select'),
    path('osm_railmap_county/<str:county>/', views.osm_railmap_county, name='osm_railmap_county'),

    path('trackmap/', views_wip.Trackmap.as_view(), name='trackmap'),

    path('depots_vis_timeline/', views_wip.depot_vis_timeline, name='depot_vis_timeline'),

    path('heritage_sites/', views.HeritageSiteListView.as_view(), name='heritage_sites'),
    path('heritage_site/<int:heritage_site_id>/', views.heritage_site, name='heritage_site'),

    path('visits/', views.VisitListView.as_view(), name='visits'),
    path('visit/<int:visit_id>/', views.visit, name='visit'),
    ]