from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *

# @admin.register(UkAdminBoundaries)
# class UkAdminBoundariesAdmin(OSMGeoAdmin):
#     list_display = ['ctyua19cd', 'ctyua19nm']
#     search_fields = ['ctyua19nm']
#     ordering = ['ctyua19nm']
#     verbose_name = "UK Administrative Boundaries"


@admin.register(GdUkAlwaysOpenLand)
class GdUkAlwaysOpenLandAdmin(OSMGeoAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "UK National Trust Always Open Land Area"


@admin.register(GdUkParksGardens)
class GdUkParksGardensAdmin(OSMGeoAdmin):
    list_display = ["listentry", "name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "Historic England Parks and Gardens Listing"


@admin.register(GdUkScheduledMonuments)
class GdUkScheduledMonumentsAdmin(OSMGeoAdmin):
    list_display = ["listentry", "name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "Historic England Scheduled Monuments Listings"


@admin.register(GdUkListedBuildings)
class GdUkListedBuildingsAdmin(OSMGeoAdmin):
    list_display = ("listentry", "name", "location", "grade")
    search_fields = ["name", "location"]
    list_filter = ["grade"]
    ordering = ["name"]
    verbose_name = "Historic England Listed Buildings"


@admin.register(MyPlaces)
class MyPlaces(OSMGeoAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "My Places"
