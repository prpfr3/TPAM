from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import *
from .forms import *

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
