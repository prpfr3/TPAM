from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
    path("", views.index, name="index"),
    path("routes_southern", views.routes_southern, name="routes_southern"),
    path("locations/", views.locations, name="locations"),
    path("location/<int:location_id>/", views.location, name="location"),
    path("location_area/<slug:slug>/", views.location_area, name="location_area"),
    path("routes/", views.routes, name="routes"),
    path("routes_timeline/", views.routes_timeline, name="routes_timeline"),
    path("route/<int:route_id>/", views.route, name="route"),
    path("route_storymap/<slug>/", views.route_storymap, name="route_storymap"),
    path("route_map/<slug>/", views.route_map, name="route_map"),
    path("route_timeline/<slug>/", views.route_timeline, name="route_timeline"),
    path(
        "closed_lines_region_select/",
        views.ClosedLinesRegionSelectView.as_view(),
        name="closed_lines_region_select",
    ),
    # path(
    #     "map_closed_lines/<str:geo_area>/",
    #     views.MapClosedLines.as_view(),
    #     name="map_closed_lines",
    # ),
    path("elrs/", views.elrs, name="elrs"),
    path("elr_map/<int:elr_id>/", views.elr_map, name="elr_map"),
    path("elr_storymap/<int:elr_id>/", views.elr_storymap, name="elr_storymap"),
    path("elr_history/<int:elr_id>/", views.elr_history, name="elr_history"),
    path(
        "elr_display_osmdata/<int:elr_id>/",
        views.elr_display_osmdata,
        name="elr_display_osmdata",
    ),
    path(
        "regional_map_select/",
        views.RegionalMapSelectView.as_view(),
        name="regional_map_select",
    ),
    path(
        "regional_map/<str:geo_area>/",
        views.regional_map,
        name="regional_map",
    ),
    path("trackmap/", views.Trackmap.as_view(), name="trackmap"),
    # path(
    #     "heritage_sites/", views.HeritageSiteListView.as_view(), name="heritage_sites"
    # ),
    # path(
    #     "heritage_site/<int:heritage_site_id>/",
    #     views.heritage_site,
    #     name="heritage_site",
    # ),
    path("visits/", views.VisitListView.as_view(), name="visits"),
    path("visit/<int:visit_id>/", views.visit, name="visit"),

]
