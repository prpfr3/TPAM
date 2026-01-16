from django.contrib import admin
from rtt.models import NaPTANRailReferences
from django.db import models


class NaPTANRailReferencesAdmin(admin.ModelAdmin):
    list_display = ["atcocode", "tiploccode",
                    "crscode", "name", "easting", "northing"]
    search_fields = ("atcocode", "tiploccode", "crscode", "name")
    ordering = ('crscode', 'tiploccode')

admin.site.register(NaPTANRailReferences, NaPTANRailReferencesAdmin)