from django.contrib import admin
from locos.models import *
from tinymce.widgets import TinyMCE
from django.db import models


class LocoClassAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "brdslug"]
    list_filter = [
        "br_power_class",
        "wheel_body_type",
        ("owner_operators", admin.RelatedOnlyFieldListFilter),
        ("manufacturers", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["name"]
    ordering = ["name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = ["designer_person"]
    filter_horizontal = ["references", "owner_operators", "manufacturers", "posts"]
    show_facets = admin.ShowFacets.ALWAYS


class LocomotiveAdmin(admin.ModelAdmin):
    list_display = [
        "lococlass",
        "number_as_built",
        "number_pregrouping_1",
        "number_grouping_1",
        "number_postgrouping_1",
    ]
    list_filter = ["company_pregrouping_code", "company_grouping_code", "manufacturer"]
    search_fields = (
        "number_as_built",
        "number_pregrouping_1",
        "number_grouping_1",
        "number_postgrouping_1",
        "lococlass__name",
    )
    ordering = ("number_as_built",)


class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ("whyte_notation",)


class ImageAdmin(admin.ModelAdmin):
    list_display = ["image_thumbnail", "image_name", "location", "visit"]
    list_filter = [
        ("location", admin.RelatedOnlyFieldListFilter),
        ("visit", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["image_name"]
    ordering = ["image_name"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = ["location"]
    filter_horizontal = ["lococlass"]

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return ""

    image_thumbnail.short_description = "Thumbnail"


admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(Image, ImageAdmin)
