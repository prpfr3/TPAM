from django.contrib import admin
from .models import SlideHeader, Slide, Slidepack
from tinymce.widgets import TinyMCE
from django.db import models


class SlidepackAdmin(admin.ModelAdmin):
    raw_id_fields = ("slideheader_fk",)
    autocomplete_fields = ["slide_fk"]
    search_fields = ["slide__text_headline"]


class SlideAdmin(admin.ModelAdmin):
    ordering = ["text_headline"]
    search_fields = ["text_headline"]
    formfield_overrides = {
        models.TextField: {
            "widget": TinyMCE(
                attrs={"cols": 80, "rows": 30},
            )
        },
    }


admin.site.register(SlideHeader)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Slidepack, SlidepackAdmin)
