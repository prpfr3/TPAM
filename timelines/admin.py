from django.contrib import admin

from .models import TimelineSlideHeader, TimelineSlide, TimelineSlidepack


class TimelineSlidepackAdmin(admin.ModelAdmin):
    # list_display = ['routemap', 'loc_no', 'label', 'location_fk']
    raw_id_fields = ("slideheader_fk",)
    autocomplete_fields = ["slide_fk"]
    search_fields = ["slide__text_headline"]


class TimelineSlideAdmin(admin.ModelAdmin):
    ordering = ["text_headline"]
    search_fields = ["text_headline"]


admin.site.register(TimelineSlideHeader)
admin.site.register(TimelineSlide, TimelineSlideAdmin)
admin.site.register(TimelineSlidepack, TimelineSlidepackAdmin)
