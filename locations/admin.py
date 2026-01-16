from django.db import models
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.contenttypes.admin import GenericInlineModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from .forms import LocationAdminForm
from .models import *
from utils.utils import custom_slugify
from tinymce.widgets import TinyMCE

if settings.GDAL_INSTALLED:
    from django.contrib.gis.admin import GISModelAdmin

    admin_class_for_geoclasses = GISModelAdmin
else:
    admin_class_for_geoclasses = admin.ModelAdmin


class CategoriesFilter(admin.SimpleListFilter):
    title = "Categories"
    parameter_name = "categories"
    search_field = "categories__category"

    def lookups(self, request, model_admin):
        categories = LocationCategory.objects.all()
        return [(category.id, category.category) for category in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__id=self.value())

class LocationCategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]
    ordering = ["category"]
    search_fields = ["category"]
    
class LocationHistoricEventInline(GenericTabularInline):
    model = LocationHistoricEvent
    extra = 1  # Makes one blank form appear for adding new inline events
    classes = ["collapse"]  # Use 'classes' to allow collapsing if the history gets long
    fields = ("event_type", "description", "displaydate", "datefield")
    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"size": "60"})},
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event_type":
            # Sort first by category, then alphabetically by label
            kwargs["queryset"] = EventType.objects.order_by("category", "code")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form


class HistoricEventInline(GenericTabularInline):
    model = LocationHistoricEvent
    extra = 1

    # Define which fields to show in the row
    fields = ("event_type", "datefield", "displaydate", "description")


class ELRAdmin(admin.ModelAdmin):
    list_display = ["itemAltLabel", "itemLabel", "item"]
    ordering = ["itemAltLabel"]
    search_fields = ["itemLabel", "itemAltLabel"]
    list_filter = ["derived"]
    autocomplete_fields = ["owneroperators", "references"]
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


class LocationAdmin(GISModelAdmin):
    form = LocationAdminForm

    list_display = ["slug", "name", "wikiname", "wikislug", "osm_node"]
    inlines = [LocationHistoricEventInline]
    list_filter = ["source", "categories"]
    search_fields = ["wikiname", "name", "osm_node", "RCH_StopsGB_Altnames"]
    ordering = ["wikiname"]
    verbose_name = "Railway Locations"

    try:
        show_facets = admin.ShowFacets.ALWAYS
    except Exception:
        pass

    autocomplete_fields = [
        "posts",
        "references",
        "owner_operators",
        "categories",
    ]

    """ The Purpose of fieldsets


    Fieldsets serves three main organizational purposes:

    Grouping: You can group related fields under a section header (e.g. in a "Relations" section).

    Visual Hierarchy: It allows you to use the 'classes': ('collapse',) option to hide bulky data (like raw geometry or long notes) behind a clickable "Show" link.

    Layout Control: You can display multiple fields on a single line by nesting them in a tuple, e.g., ("latitude", "longitude"),.

    How to show "All Fields"
    If your goal is to show every single field on the model without manually maintaining a list, you have two options:

    1. Remove fieldsets entirely
    If you delete the fieldsets block, Django defaults to showing every editable field in the order they are defined in your models.py.

    2. Use fields instead
    If you don't care about the headers ("Relations", etc.) but want to control the order or exclude just one or two items, use the fields attribute instead of fieldsets:
    """
    # fieldsets = (
    #     (
    #         None,
    #         {
    #             "fields": (
    #                 "name",
    #                 "slug",
    #                 "wikiname",
    #                 "wikislug",
    #                 "osm_node",
    #                 "latitude",
    #                 "longitude",
    #                 "opened",
    #                 "closed",
    #                 "geometry",
    #                 "notes",
    #             )
    #         },
    #     ),
    #     (
    #         "Relations",
    #         {
    #             "fields": (
    #                 "posts",
    #                 "references",
    #                 "owner_operators",
    #                 "categories",
    #             )
    #         },
    #     ),
    # )

    def get_readonly_fields(self, request, obj=None):
        return ["slug"] if obj else []

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.filter(pk=obj.pk).first()
            if old_obj and old_obj.name != obj.name:
                obj.slug = custom_slugify(obj.name)
        else:
            if not obj.slug:
                obj.slug = custom_slugify(obj.name)

        super().save_model(request, obj, form, change)


class LocationCodeAdmin(admin.ModelAdmin):
    list_display = [
        "location_fk",
        "location_code",
        "from_date",
        "to_date",
    ]
    ordering = ["location_fk", "from_date"]
    search_fields = ["location_fk", "location_code"]


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
    inlines = [LocationHistoricEventInline]
    search_fields = ["name"]
    ordering = ["name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    autocomplete_fields = [
        "wikipedia_routemaps",
        "elrs",
        "references",
        "owneroperators",
        "posts",
    ]

    show_facets = admin.ShowFacets.ALWAYS

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        # This targets the 'size' attribute of the HTML select box
        form_field.widget.attrs.update({"size": "2"})
        return form_field


class RouteLocationAdmin(admin_class_for_geoclasses):
    # list_display = ["routemap", "loc_no", "label", "get_location_fk_field"]
    list_display = [
        "routemap",
        "loc_no",
        "label",
    ]
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
admin.site.register(EventType)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationCategory, LocationCategoryAdmin)
admin.site.register(LocationCode, LocationCodeAdmin)
admin.site.register(LocationHistoricEvent)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteGeoClosed, RouteGeoClosedAdmin)
admin.site.register(RouteGeoOsm, RouteGeoOsmAdmin)
admin.site.register(RouteGeoOsmhistory, RouteGeoOsmhistoryAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
admin.site.register(RouteCategory)
admin.site.register(UKArea)
admin.site.register(Visit, VisitAdmin)
