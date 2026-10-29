from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.admin import GISModelAdmin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from .forms import LocationAdminForm, NarrowTinyMCE
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


class LocationHistoricEventInlineForm(forms.ModelForm):
    class Meta:
        model = LocationHistoricEvent
        fields = "__all__"
        widgets = {
            "description": NarrowTinyMCE(attrs={"class": "tinymce-editor"}),
        }
    
    class Media:
        js = (
            'tinymce/tinymce.min.js',
            'tinymce/jquery.tinymce.min.js',
        )


class LocationHistoricEventInline(GenericTabularInline):
    model = LocationHistoricEvent
    form = LocationHistoricEventInlineForm
    extra = 1
    classes = ["collapse"]

    class Media:
        js = (
            'tinymce/tinymce.min.js',
            'tinymce/jquery.tinymce.min.js',
        ) + (
            'js/tinymce_init.js',
        )


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "event_type":
            kwargs["queryset"] = EventType.objects.order_by("category", "code")
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(
                app_label="locations", model__in=["location", "route"]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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


class RouteAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = [
        ("owneroperators", admin.RelatedOnlyFieldListFilter),
    ]
    inlines = [LocationHistoricEventInline]
    search_fields = ["name"]
    ordering = ["name"]
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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "notes":
            kwargs["widget"] = TinyMCE(attrs={"class": "tinymce-editor"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    class Media:
        js = (
            'tinymce/tinymce.min.js',
            'tinymce/jquery.tinymce.min.js',
        ) + (
            'js/tinymce_init.js',
        )


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


class RouteLocationAdmin(admin_class_for_geoclasses):

    list_display = [
        "routemap",
        "linear_reference",
        "loc_no",
    ]
    search_fields = ["routemap__name"]
    ordering = ["routemap", "loc_no"]
    raw_id_fields = ["routemap", "location_fk"]

    # def loc_no_display(self, obj):
    #     from .models import Location
    #     try:
    #         location = Location.objects.get(id=obj.location_fk)
    #         return f"{obj.location_fk} – {location.name}"
    #     except Location.DoesNotExist:
    #         return str(obj.location_fk)

    # loc_no_display.admin_order_field = "loc_no_display"
    # loc_no_display.short_description = "Location"



class LocationHistoricEventAdmin(admin.ModelAdmin):
    list_display = [
        "content_type",
        "related_object_link",
        "event_type", 
        "datefield", 
        "displaydate", 
        "description"
    ]
    list_filter = ["event_type", "content_type"]
    search_fields = ["location__name", "description"]
    ordering = ["location", "datefield"]

    @admin.display(description="Related Object")
    def related_object_link(self, obj):
        if obj.content_object:
            # Dynamically fetch the admin URL for the related object's model type
            try:
                url = reverse(
                    f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change",
                    args=[obj.object_id]
                )
                return format_html('<a href="{}">{}</a>', url, obj.content_object)
            except Exception:
                # Fallback if the related model isn't registered in the admin
                return str(obj.content_object)
        return "-"
    
    def get_queryset(self, request):
            queryset = super().get_queryset(request)
            # Prefetches the generic foreign key objects in bulk
            return queryset.prefetch_related('content_object')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit content_type choices in the admin form
        if db_field.name == "content_type":
            kwargs["queryset"] = ContentType.objects.filter(
                app_label="locations", model__in=["location", "route"]
            )
        if db_field.name == "event_type":
            kwargs["queryset"] = EventType.objects.order_by("category", "code")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
admin.site.register(EventType)
admin.site.register(HeritageSite, HeritageSiteAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(LocationCategory, LocationCategoryAdmin)
admin.site.register(LocationCode, LocationCodeAdmin)
admin.site.register(LocationHistoricEvent, LocationHistoricEventAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(RouteGeoClosed, RouteGeoClosedAdmin)
admin.site.register(RouteGeoOsm, RouteGeoOsmAdmin)
admin.site.register(RouteGeoOsmhistory, RouteGeoOsmhistoryAdmin)
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
admin.site.register(RouteCategory)
admin.site.register(UKArea)
admin.site.register(Visit, VisitAdmin)