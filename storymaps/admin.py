from django.contrib import admin
from .models import *
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


class TimelineSlidepackAdmin(admin.ModelAdmin):
    # list_display = ['routemap', 'loc_no', 'label', 'location_fk']
    raw_id_fields = ("slideheader_fk",)
    autocomplete_fields = ["slide"]
    search_fields = ["slide__text_headline"]


class CarouselpackAdmin(admin.ModelAdmin):
    raw_id_fields = ("slideheader_fk",)
    autocomplete_fields = ["slide_fk"]
    search_fields = ["slide__text_headline"]


admin.site.register(TimelineSlideHeader)
admin.site.register(TimelineSlidepack, TimelineSlidepackAdmin)
admin.site.register(SlideHeader)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Slidepack, SlidepackAdmin)
admin.site.register(CarouselHeader)
admin.site.register(Carouselpack, CarouselpackAdmin)
