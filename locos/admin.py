from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from locos.models import *
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

class LocationsAdmin(OSMGeoAdmin):
    list_display = ['wikiname', 'wikislug']
    search_fields = ['wikiname']
    ordering = ['wikiname']
    verbose_name = "Railway Stations from Wikipedia/Naptan"

class DepotsAdmin(admin.ModelAdmin):
    list_display = ["depot", "codes", "code_dates"]
    list_filter = ['br_region']
    search_fields = ('depot', 'codes')
    ordering = ('codes', 'depot')
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    #prepopulated_fields = {'code_dates': ('title',)}    
    #raw_id_fields = ('codes',)    
    #date_hierarchy = 'code_dates'    
    #fields = ["date_added", "text", "eng_name"]
    #fieldsets = [
    #("Groupings", {'fields': ["a", "b", "c", "d"]}),
    #("Timestamp", {"fields": ["datefield"]})
    #]

class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "code", ]
    ordering = ('name',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "birthdate", "dieddate", "wikitextslug",]
    ordering = ('name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role",]
    ordering = ('role',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ["person", "role",]
    ordering = ('person',)
    list_filter = ["role", "person",]
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class ImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'image', 'location', 'notes', 'date_added']
    ordering = ('image_name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocoClassAdmin(admin.ModelAdmin):
    list_display = ["grouping_class", "grouping_company", "pre_grouping_class", "pre_grouping_company",  "wheel_body_type"]
    list_filter = ['grouping_company', 'pre_grouping_company', 'br_power_class', 'wheel_body_type']
    search_fields = ('grouping_class', 'pre_grouping_class')
    ordering = ['grouping_company', 'pre_grouping_company', 'grouping_class']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
 
class ModernClassAdmin(admin.ModelAdmin):
    list_display = ["modern_class", "aka_class", "wheel_id"]
    list_filter = ['transmission', 'builder']
    search_fields = ['modern_class']
    ordering = ['modern_class']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocomotiveAdmin(admin.ModelAdmin):
    list_display = ["number", "pre_grouping_class"]
    list_filter = ['pre_grouping_class']
    search_fields = ('pre_grouping_class', 'number')
    ordering = ('pre_grouping_class', 'number')

class BuilderAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "pre_grouping_owner", "grouping_owner", "date_opened", "date_closed", "railuk_builder_code", "railuk_builder_code", ]
    search_fields = ["name"]
    ordering = ["name"]

class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ('whyte_notation', )

admin.site.register(Depots, DepotsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(PersonRole,PersonRoleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(ModernClass, ModernClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(Sighting)
admin.site.register(LocoSighting)
admin.site.register(LocoClassSighting)
admin.site.register(SlideHeader)
admin.site.register(Slide)
admin.site.register(Slidepack)
admin.site.register(Locations, LocationsAdmin)
