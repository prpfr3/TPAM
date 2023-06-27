from django.contrib import admin

# from django.contrib.gis.admin import OSMGeoAdmin
from locations.models import *
from tinymce.widgets import TinyMCE
from django.db import models


class DepotAdmin(admin.ModelAdmin):
    list_display = ["depot", "code", "date_start", "date_end"]
    list_filter = ["br_region"]
    search_fields = ("depot", "code")
    ordering = ("depot", "date_start")
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class ELRAdmin(admin.ModelAdmin):
    list_display = ["item", "itemLabel", "itemAltLabel"]
    ordering = ["itemAltLabel"]
    search_fields = ["itemLabel", "itemAltLabel"]


class LocationAdmin(admin.ModelAdmin):
    # class LocationAdmin(OSMGeoAdmin):
    list_display = ["name", "wikiname", "wikislug", "osm_node", "elr_fk"]
    list_filter = ["type"]
    search_fields = ["wikiname", "name"]
    ordering = ["wikiname"]
    verbose_name = "Railway Locations"
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 30},
            )
        },
    }
    filter_horizontal = ["references"]
    raw_id_fields = ["elr_fk", "post_fk"]


class LocationEventAdmin(admin.ModelAdmin):
    list_display = ["route_fk", "date", "datefield", "type", "description"]
    ordering = ["route_fk", "datefield"]
    search_fields = ["route_fk", "date"]


# @admin.register(RouteGeoClosed)
# class RouteGeoClosedAdmin(admin.ModelAdmin):
#     # class RouteGeoClosedAdmin(OSMGeoAdmin):
#     list_display = ['name', 'description']
#     search_fields = ['name', 'description']
#     ordering = ['name']
#     verbose_name = "Closed Lines from Google Map"


@admin.register(RouteGeoOsm)
class RouteGeoOsmAdmin(admin.ModelAdmin):
    # class RouteGeoOsmAdmin(OSMGeoAdmin):
    list_display = ["name"]
    search_fields = ["name", "type"]
    ordering = ["name"]
    verbose_name = "OSM Current Map Rail Routes"


@admin.register(RouteGeoOsmhistory)
class RouteGeoOsmAdmin(admin.ModelAdmin):
    # class RouteGeoOsmhistoryAdmin(OSMGeoAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "OSM History Rail Routes"


class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "wikipedia_slug"]
    search_fields = ["name"]
    ordering = ["name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = [
        "post_fk",
    ]
    filter_horizontal = ["wikipedia_routemaps", "elrs", "references", "owneroperators"]


class RouteLocationAdmin(admin.ModelAdmin):
    # class RouteLocationAdmin(OSMGeoAdmin):
    list_display = ["routemap", "loc_no", "label", "location_fk"]
    search_fields = ["routemap__name", "label"]
    ordering = ["routemap", "loc_no"]
    raw_id_fields = ["routemap", "location_fk"]


class ELRLocationAdmin(admin.ModelAdmin):
    # class ELRLocationAdmin(OSMGeoAdmin):
    list_display = ["elr_fk", "location_fk", "distance"]
    search_fields = [
        "elr_fk__itemLabel",
        "elr_fk__itemAltLabel",
        "location_fk__wikiname",
        "location_fk__name",
    ]
    ordering = ["elr_fk", "distance", "location_fk"]
    raw_id_fields = ["elr_fk", "location_fk"]


class RouteMapAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):
    list_display = ["tpam_type", "type", "name", "wikislug", "url", "type"]
    list_filter = ["tpam_type", "type"]
    ordering = ("name",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "date", "notes"]
    ordering = ("date",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = ["location"]


admin.site.register(Depot, DepotAdmin)
admin.site.register(ELR, ELRAdmin)
admin.site.register(ELRLocation, ELRLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationEvent, LocationEventAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
