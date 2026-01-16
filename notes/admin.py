from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import *
from .forms import PostForm, ReferenceAdminForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ["title", "slug", "topic", "owner", "publish", "status"]
    list_filter = ["status", "created", "publish", "owner"]
    search_fields = ["title", "body"]
    raw_id_fields = ("owner",)
    date_hierarchy = "publish"
    autocomplete_fields = ["references"]

    def get_readonly_fields(self, request, obj=None):
        return ["slug"] if obj else []

    def save_model(self, request, obj, form, change):
        if change:  # Check if this is an update of an existing object
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.title != obj.title:  # If the title has changed
                obj.slug = custom_slugify(obj.title)
        elif not obj.slug:
            obj.slug = custom_slugify(obj.title)

        if not change:
            # This means the object is being created, so set the owner
            obj.owner = request.user
        obj.save()


@admin.register(Reference)
# Lookups are defined in notes.forms as ReferenceAdminForm
class ReferenceAdmin(admin.ModelAdmin):

    form = ReferenceAdminForm

    search_fields = ["full_reference", "image"]
    list_display = ["type", "journal", "year", "issue", "pages", "title"]
    # list_display = ["full_reference", "image"]
    list_filter = ["type", "journal"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
