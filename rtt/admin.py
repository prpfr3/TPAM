from django.contrib import admin
from rtt.models import NaPTANRailReferences
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

class NaPTANRailReferencesAdmin(admin.ModelAdmin):
    list_display = ["atcocode", "tiploccode", "crscode", "stationname", "easting", "northing"]
    #list_filter = ['']
    search_fields = ("atcocode", "tiploccode", "crscode", "stationname")
    ordering = ('crscode', 'tiploccode')
    #formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    #prepopulated_fields = {'code_dates': ('title',)}    
    #raw_id_fields = ('codes',)    
    #date_hierarchy = 'code_dates'   
    #fields = ["date_added", "text", "eng_name"]
    #fieldsets = [
    #("Groupings", {'fields': ["a", "b", "c", "d"]}),
    #("Timestamp", {"fields": ["datefield"]})
    #]

admin.site.register(NaPTANRailReferences, NaPTANRailReferencesAdmin)