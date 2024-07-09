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
        "lococlass",
        "number_as_built",
        "identifier",
        "number_pregrouping_1",
        "number_grouping_1",
        "number_postgrouping_1",
    ]
    list_filter = ["company_pregrouping_code", "company_grouping_code", "manufacturer"]
    search_fields = (
        "number_as_built",
        "identifier",
        "number_pregrouping_1",
        "number_grouping_1",
        "number_postgrouping_1",
        "lococlass__wikiname",
    )
    ordering = ("number_as_built",)


class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ("whyte_notation",)


admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(LocoClassList, LocoClassListAdmin)
