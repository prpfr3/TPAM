from django.contrib import admin
from .models import *
from .forms import PostForm
from django.db import models
from tinymce.widgets import TinyMCE
from locos.models import LocoClass
from companies.models import Company
from django.utils.html import format_html


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

        if not change:
            # This means the object is being created, so set the owner
            obj.owner = request.user
        obj.save()


class LocoClassInline(admin.TabularInline):
    model = LocoClass.references.through
    extra = 1  # Number of empty forms to display


class CompanyInline(admin.TabularInline):
    model = Company.references.through
    extra = 1  # Number of empty forms to display


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ["full_reference", "image"]
    list_display = ["full_reference", "image"]
    list_filter = ["type"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    inlines = [LocoClassInline, CompanyInline]


@admin.register(BRMPhotos)
class BRMPhotosAdmin(admin.ModelAdmin):
    list_display = ["reference_number", "company", "lococlass", "number", "location"]
    search_fields = ["reference_number", "company", "lococlass", "number", "location"]
    ordering = ("reference_number",)


@admin.register(BRMPlans)
class BRMPlansAdmin(admin.ModelAdmin):
    list_display = ["archivenumber", "location", "description", "tube"]
    search_fields = ["archivenumber", "location", "description", "tube"]
    ordering = ("location",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    actions = ["delete_selected"]

    def changelist_view(self, request, extra_context=None):
        # Call the parent changelist_view method to ensure the data is loaded
        response = super().changelist_view(request, extra_context)

        # Check if 'result_list' contains data (debugging purposes)
        if hasattr(response, "context_data") and "cl" in response.context_data:
            changelist = response.context_data["cl"]
            print(
                f"Result count: {len(changelist.result_list)}"
            )  # Debugging line to check result count

        return response

    def get_changelist(self, request, **kwargs):
        """
        Override the changelist view to add filter options in the table header.
        """
        from django.contrib.admin.views.main import ChangeList

        class CustomChangeList(ChangeList):
            def get_results(self, request):
                # Call the original get_results method
                super().get_results(request)

                # Add custom logic for displaying filters in the header row
                self.result_list = self.queryset  # Add filtering logic if needed

        return CustomChangeList
