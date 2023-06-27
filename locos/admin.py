from django.contrib import admin
from locos.models import *
from tinymce.widgets import TinyMCE
from django.db import models


class LocoClassAdmin(admin.ModelAdmin):
    list_display = ["wikiname", "brdslug", "wheel_body_type"]
    list_filter = [
        "br_power_class",
        "wheel_body_type",
        ("owner_operators", admin.RelatedOnlyFieldListFilter),
        ("manufacturers", admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ["wikiname"]
    ordering = ["wikiname"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    raw_id_fields = ["post_fk", "designer_person"]
    filter_horizontal = ["references", "owner_operators", "manufacturers"]


class LocoClassListAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "brdslug", "lococlass_fk"]
    search_fields = ["name", "wikislug"]
    ordering = ["name"]
    raw_id_fields = [
        "lococlass_fk",
    ]


class LocomotiveAdmin(admin.ModelAdmin):
    list_display = [
        "identifier",
        "number_pregrouping",
        "number_grouping",
        "number_postgrouping",
    ]
    list_filter = ["company_pregrouping_code", "company_grouping_code", "manufacturer"]
    search_fields = (
        "identifier",
        "number_pregrouping",
        "number_grouping",
        "number_postgrouping",
    )
    ordering = ("identifier",)


class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ("whyte_notation",)


admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(LocoClassList, LocoClassListAdmin)
