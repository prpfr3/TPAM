from django.contrib import admin
from .models import *
from .forms import PostForm
from django.db import models
from tinymce.widgets import TinyMCE
from locos.models import LocoClass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ["title", "slug", "topic", "owner", "publish", "status"]
    list_filter = ["status", "created", "publish", "owner"]
    search_fields = ["title", "body"]
    raw_id_fields = ("owner",)
    date_hierarchy = "publish"
    filter_horizontal = ["references"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["slug"]
        else:
            return []

    def save_model(self, request, obj, form, change):
        if change:  # Check if this is an update of an existing object
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.title != obj.title:  # If the title has changed
                obj.slug = custom_slugify(obj.title)
        else:
            if not obj.slug:
                obj.slug = custom_slugify(obj.title)
        obj.save()


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
