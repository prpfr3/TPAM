from locations.models import *
from tinymce.widgets import TinyMCE
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.gis import forms
from django.contrib.gis.db.models import GeometryField

from django.contrib.gis.admin import GISModelAdmin

if settings.GDAL_INSTALLED:
    from django.contrib.gis.admin import GISModelAdmin

    admin_class_for_geoclasses = GISModelAdmin
else:
    admin_class_for_geoclasses = admin.ModelAdmin


class CategoriesFilter(admin.SimpleListFilter):
    title = "Categories"
    parameter_name = "categories"

    def lookups(self, request, model_admin):
        categories = LocationCategory.objects.all()
        return [(category.id, category.category) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id=self.value())


class ELRAdmin(admin.ModelAdmin):
    list_display = ["itemAltLabel", "itemLabel", "item"]
    ordering = ["itemAltLabel"]
    search_fields = ["itemLabel", "itemAltLabel"]
    list_filter = ["derived"]
    filter_horizontal = ["owneroperators", "references"]
    raw_id_fields = ["start_point", "end_point"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only select the fields you need for the list view
        return qs.only("itemAltLabel", "itemLabel", "item")


class ELRLocationAdmin(admin_class_for_geoclasses):
    list_display = ["elr_fk", "location_fk", "distance"]
    search_fields = [
        "elr_fk__itemLabel",
        "elr_fk__itemAltLabel",
        "location_fk__wikiname",
        "location_fk__name",
    ]
    ordering = [
        "elr_fk__itemAltLabel",
        "elr_fk__itemLabel",
        "elr_fk__item",
        "distance",
        "location_fk__name",
    ]
    raw_id_fields = ["elr_fk", "location_fk"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Only select the necessary fields from the related `elr_fk` table for performance
        return qs.select_related("elr_fk", "location_fk").only(
            "elr_fk__itemAltLabel",
            "elr_fk__itemLabel",
            "elr_fk__item",
            "location_fk__name",
            "distance",
        )


class HeritageSiteAdmin(admin.ModelAdmin):
    list_display = ["tpam_type", "type", "name", "wikislug", "url", "type"]
    list_filter = ["tpam_type", "type"]
    search_fields = ("name",)
    ordering = ("name",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class LocationAdmin(admin_class_for_geoclasses):
    list_display = ["name", "slug", "wikiname", "wikislug", "osm_node"]
    list_filter = ["source", CategoriesFilter]
    search_fields = ["wikiname", "name", "osm_node", "RCH_StopsGB_Altnames"]
    ordering = ["wikiname"]
    verbose_name = "Railway Locations"

    filter_horizontal = [
        "posts",
        "references",
        "owner_operators",
        "categories",
    ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "notes" and isinstance(db_field, models.TextField):
            kwargs["widget"] = TinyMCE()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["slug"]
        else:
            return []

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.name != obj.name:  # If the title has changed
                obj.slug = custom_slugify(obj.name)
        else:
            if not obj.slug:
                obj.slug = custom_slugify(obj.name)
        obj.save()


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
        "elr_fk__itemLabel",
        "date",
    ]
    raw_id_fields = ["route_fk", "company_fk", "location_fk", "elr_fk"]


class RouteGeoClosedAdmin(admin_class_for_geoclasses):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]
    ordering = ["name"]
    verbose_name = "Closed Lines from Google Map"


class RouteGeoOsmAdmin(admin_class_for_geoclasses):
    list_display = ["name"]
    search_fields = ["name", "type"]
    ordering = ["name"]
    verbose_name = "OSM Current Map Rail Routes"


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
    filter_horizontal = [
        "wikipedia_routemaps",
        "elrs",
        "references",
        "owneroperators",
        "posts",
    ]


class RouteLocationAdmin(admin_class_for_geoclasses):
    # list_display = ["routemap", "loc_no", "label", "get_location_fk_field"]
    list_display = [
        "routemap",
        "loc_no",
        "label",
    ]
    search_fields = ["routemap__name", "label"]
    ordering = ["routemap", "loc_no"]
    # raw_id_fields = ["routemap", "location_fk"]
    raw_id_fields = ["routemap"]

    def get_location_fk_field(self, obj):
        if obj.location_fk:  # Check if location_fk is not None
            return obj.location_fk.opened
        else:
            return None

    get_location_fk_field.short_description = (
        "Opened"  # Optional: Customizing column header
    )


class RouteMapAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


class VisitAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "date", "notes"]
    ordering = ("date",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = ["location"]


admin.site.register(ELR, ELRAdmin)
admin.site.register(ELRLocation, ELRLocationAdmin)
admin.site.register(HeritageSite, HeritageSiteAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationCategory)
admin.site.register(LocationCode, LocationCodeAdmin)
admin.site.register(LocationEvent, LocationEventAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteGeoClosed, RouteGeoClosedAdmin)
admin.site.register(RouteGeoOsm, RouteGeoOsmAdmin)
admin.site.register(RouteGeoOsmhistory, RouteGeoOsmhistoryAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
admin.site.register(RouteCategory)
admin.site.register(UKArea)
admin.site.register(Visit, VisitAdmin)
