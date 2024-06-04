# from django.contrib.gis.admin import OSMGeoAdmin # For GDAL. (OSMGeoAdmin deprecated, now GIS ModelAdmin)
from locations.models import *
from tinymce.widgets import TinyMCE
from django.db import models
from django.conf import settings
from django.contrib import admin

if settings.GDAL_INSTALLED:
    from django.contrib.gis.admin import GISModelAdmin

    class CustomGeoWidgetAdmin(GISModelAdmin):
        gis_widget_kwargs = {
            "attrs": {
                "default_zoom": 8,
                "default_lon": 0,
                "default_lat": 51.5,
            },
        }

    admin_class_for_geoclasses = CustomGeoWidgetAdmin
else:
    admin_class_for_geoclasses = admin.ModelAdmin


class ELRAdmin(admin.ModelAdmin):
    list_display = ["slug", "item", "itemLabel", "itemAltLabel"]
    ordering = ["itemAltLabel"]
    search_fields = ["itemLabel", "itemAltLabel"]


class CategoriesFilter(admin.SimpleListFilter):
    title = "Categories"
    parameter_name = "categories"

    def lookups(self, request, model_admin):
        categories = LocationCategory.objects.all()
        return [(category.id, category.category) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id=self.value())


class LocationAdmin(admin_class_for_geoclasses):
    list_display = ["slug", "name", "wikiname", "wikislug", "osm_node"]
    list_filter = ["source", CategoriesFilter]
    search_fields = ["wikiname", "name", "osm_node"]
    ordering = ["wikiname"]
    verbose_name = "Railway Locations"
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 30},
            )
        },
    }
    filter_horizontal = [
        "posts",
        "references",
        "owner_operators",
        "categories",
    ]


class LocationCodeAdmin(admin.ModelAdmin):
    list_display = [
        "location_fk",
        "location_code",
        "from_date",
        "to_date",
    ]
    ordering = ["location_fk", "from_date"]
    search_fields = ["location_fk", "location_code"]


class LocationEventAdmin(admin.ModelAdmin):
    list_display = [
        "company_fk",
        "route_fk",
        "location_fk",
        "date",
        "datefield",
        "type",
        "description",
    ]
    ordering = ["route_fk", "datefield"]
    search_fields = [
        "route_fk__name",
        "company_fk__name",
        "location_fk__name",
        "elr_fk__name",
        "date",
    ]
    raw_id_fields = ["route_fk", "company_fk", "location_fk", "elr_fk"]


# @admin.register(RouteGeoClosed)
# class RouteGeoClosedAdmin(admin_class_for_geoclasses):
#     list_display = ['name', 'description']
#     search_fields = ['name', 'description']
#     ordering = ['name']
#     verbose_name = "Closed Lines from Google Map"


@admin.register(RouteGeoOsm)
class RouteGeoOsmAdmin(admin_class_for_geoclasses):
    list_display = ["name"]
    search_fields = ["name", "type"]
    ordering = ["name"]
    verbose_name = "OSM Current Map Rail Routes"


@admin.register(RouteGeoOsmhistory)
class RouteGeoOsmhistoryAdmin(admin_class_for_geoclasses):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]
    verbose_name = "OSM History Rail Routes"


class RouteAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = [
        ("owneroperators", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name"]
    ordering = ["name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = [
        "post_fk",
    ]
    filter_horizontal = ["wikipedia_routemaps", "elrs", "references", "owneroperators"]


class RouteSectionAdmin(admin.ModelAdmin):
    list_display = ["route_fk", "name"]
    search_fields = ["route_fk", "name"]
    ordering = ["name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class RouteLocationAdmin(admin_class_for_geoclasses):
    list_display = ["routemap", "loc_no", "label", "get_location_fk_field"]
    search_fields = ["routemap__name", "label"]
    ordering = ["routemap", "loc_no"]
    raw_id_fields = ["routemap", "location_fk"]

    def get_location_fk_field(self, obj):
        if obj.location_fk:  # Check if location_fk is not None
            return obj.location_fk.opened
        else:
            return None

    get_location_fk_field.short_description = (
        "Opened"  # Optional: Customizing column header
    )


class ELRLocationAdmin(admin_class_for_geoclasses):
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


admin.site.register(ELR, ELRAdmin)
admin.site.register(ELRLocation, ELRLocationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationCategory)
admin.site.register(LocationCode, LocationCodeAdmin)
admin.site.register(LocationEvent, LocationEventAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
admin.site.register(RouteSection, RouteSectionAdmin)
admin.site.register(RouteCategory)
admin.site.register(RouteSectionELR)
admin.site.register(UKArea)
