from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from locations.models import *
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

class DepotAdmin(admin.ModelAdmin):
    list_display = ["depot", "code", "date_start", "date_end"]
    list_filter = ['br_region']
    search_fields = ('depot', 'code')
    ordering = ('depot', 'date_start')
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class ELRAdmin(admin.ModelAdmin):
    list_display = ['item', 'itemLabel', 'itemAltLabel']
    ordering = ['itemLabel']
    search_fields = ['itemLabel', 'itemAltLabel']

class LocationAdmin(OSMGeoAdmin):
    list_display = ['osm_node', 'stationname', 'wikiname', 'wikislug', 'elr_fk']
    list_filter = ['type']
    search_fields = ['wikiname']
    ordering = ['wikiname']
    verbose_name = "Railway Stations from Wikipedia/Naptan"
    formfield_overrides = {models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30},)},}

class LocationEventAdmin(admin.ModelAdmin):
    list_display = ['route_fk', 'date', 'datefield', 'type', 'description']
    ordering = ['route_fk', 'datefield']
    search_fields = ['route_fk', 'date']

@admin.register(RouteGeoClosed)
class RouteGeoClosedAdmin(OSMGeoAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']
    verbose_name = "Closed Lines from Google Map"

@admin.register(RouteGeoOsm)
class RouteGeoOsmAdmin(OSMGeoAdmin):
    list_display = ['name']
    search_fields = ['name', 'type']
    ordering = ['name']
    verbose_name = "OSM Current Map Rail Routes"

@admin.register(RouteGeoOsmhistory)
class RouteGeoOsmhistoryAdmin(OSMGeoAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    verbose_name = "OSM History Rail Routes"

class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "wikipedia_slug"]
    search_fields = ["name"]
    ordering = ["name"]

class RouteLocationAdmin(OSMGeoAdmin):
    list_display = ['routemap', 'loc_no', 'label', 'location_fk']
    search_fields = ['routemap__name', 'label']
    ordering = ['routemap', 'loc_no']

class RouteMapAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]

admin.site.register(Depot, DepotAdmin)
admin.site.register(ELR, ELRAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationEvent, LocationEventAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)