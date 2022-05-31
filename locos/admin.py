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
    search_fields = ['image_name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocoClassAdmin(admin.ModelAdmin):
    list_display = ["wikipedia_name", "wheel_body_type"]
    list_filter = ['br_power_class', 'wheel_body_type']
    search_fields = ['wikipedia_name']
    ordering = ['wikipedia_name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocomotiveAdmin(admin.ModelAdmin):
    list_display = ["number", "wikipedia_name"]
    list_filter = ['wikipedia_name']
    search_fields = ('wikipedia_name', 'number')
    ordering = ('wikipedia_name', 'number')

class BuilderAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "pre_grouping_owner", "grouping_owner", "date_opened", "date_closed", "railuk_builder_code", "railuk_builder_code", ]
    search_fields = ["name"]
    ordering = ["name"]

class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "wikipedia_slug"]
    search_fields = ["name"]
    ordering = ["name"]

class ClassBuilderAdmin(admin.ModelAdmin):
    list_display = ["lococlass_fk", "builder_fk", "person_fk", "company_fk", ]
    ordering = ["lococlass_fk"]

class RouteOwnerOperatorAdmin(admin.ModelAdmin):
    list_display = ["route_fk", "company_fk",]
    ordering = ["route_fk"]

class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ('whyte_notation', )

class SlidepackAdmin(admin.ModelAdmin):
    raw_id_fields = ('slideheader_fk',)
    autocomplete_fields = ['slide_fk']

class SlideAdmin(admin.ModelAdmin):
    ordering = ['text_headline']
    search_fields = ['text_headline']

admin.site.register(Depots, DepotsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(PersonRole,PersonRoleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(Sighting)
admin.site.register(ClassDesigner)
admin.site.register(RouteOwnerOperator, RouteOwnerOperatorAdmin)
admin.site.register(ClassBuilder, ClassBuilderAdmin)
admin.site.register(LocoSighting)
admin.site.register(LocoClassSighting)
admin.site.register(LocoClassImage)
admin.site.register(SlideHeader)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Slidepack, SlidepackAdmin)
admin.site.register(Locations, LocationsAdmin)
