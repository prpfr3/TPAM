from django.contrib import admin
from .models import *
from django.db import models
from tinymce.widgets import TinyMCE
from locos.models import LocoClass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "topic", "owner", "publish", "status"]
    list_filter = ["status", "created", "publish", "owner"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    # Creates a lookup widget for large volume lookups
    raw_id_fields = ("owner",)
    date_hierarchy = "publish"
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    filter_horizontal = ["references"]


class LocoClassInline(admin.TabularInline):
    model = LocoClass.references.through
    extra = 1  # Number of empty forms to display


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ["full_reference", "image"]
    list_display = ["full_reference", "image"]
    list_filter = ["type"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    inlines = [LocoClassInline]


@admin.register(BRMPlans)
class BRMPlansAdmin(admin.ModelAdmin):
    list_display = ["location", "description", "tube"]
    search_fields = ["location", "description", "tube"]
    ordering = ("location",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


admin.site.register(Topic)
