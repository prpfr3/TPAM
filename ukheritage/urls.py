from django.urls import path
from . import views

app_name = "ukheritage"

urlpatterns = [
    # path("", views.index, name="index"),
    # path("region_select/", views.RegionalMapSelectView.as_view(), name="region_select"),
    # path("county_select/", views.county_select, name="county_select"),
    # path("heritage_map/<geo_area>/", views.HeritageMap.as_view(), name="heritage_map"),
    # path(
    #     "listed_buildings_select/",
    #     views.listed_buildings_select,
    #     name="listed_buildings_select",
    # ),
    # path(
    #     "listed_buildings_nearby/",
    #     views.listed_buildings_nearby,
    #     name="listed_buildings_nearby",
    # ),
    # path("listed_buildings_nearby/<pk>", views.building_detail, name="building_detail"),
    # path("like-unlike/", views.like_unlike_building, name="like-unlike"),
    # path(
    #     "get_nearby_buildings/<int:num_buildings>/",
    #     views.get_nearby_buildings,
    #     name="get_nearby_buildings",
    # ),
    # path("myplaces/", views.myplaces, name="myplaces"),
    # path("myplace/<pk>", views.myplace, name="myplace"),
    # path("make_favourite/", views.make_favourite, name="make_favourite"),
    # path("get_myplaces/<int:num_places>/", views.get_myplaces, name="get_myplaces"),
]
