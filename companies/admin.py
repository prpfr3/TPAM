from django.contrib import admin
from companies.models import *
from tinymce.widgets import TinyMCE
from django.db import models


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "wikislug",
        "code",
    ]
    search_fields = ["name", "code"]
    ordering = ("name",)
    raw_id_fields = [
        "post_fk",
    ]


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "wikislug",
        "pre_grouping_owner",
        "grouping_owner",
        "date_opened",
        "date_closed",
        "railuk_code",
        "brd_code",
        "brsl_code",
    ]
    search_fields = ["name"]
    ordering = ["name"]
    raw_id_fields = [
        "post_fk",
    ]


class ClassManufacturerAdmin(admin.ModelAdmin):
    list_display = [
        "lococlass_fk",
        "manufacturer_fk",
        "person_fk",
        "company_fk",
    ]
    ordering = ["lococlass_fk"]


# admin.site.register(ClassDesigner)
# admin.site.register(ClassManufacturer, ClassManufacturerAdmin)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
