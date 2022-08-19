from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from locos.models import *
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

@admin.register(UkAdminBoundaries)
class UkAdminBoundariesAdmin(OSMGeoAdmin):
    list_display = ['ctyua19cd', 'ctyua19nm']
    search_fields = ['ctyua19nm']
    ordering = ['ctyua19nm']
    verbose_name = "UK Administrative Boundaries"

@admin.register(LocosRoutesGeoClosed)
class LocosRoutesGeoClosedAdmin(OSMGeoAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']
    verbose_name = "Closed Lines from Google Map"

@admin.register(LocosRoutesGeoOsm)
class LocosRoutesGeoOsmAdmin(OSMGeoAdmin):
    list_display = ['name']
    search_fields = ['name', 'type']
    ordering = ['name']
    verbose_name = "OSM Current Map Rail Routes"

@admin.register(LocosRoutesGeoOsmhistory)
class LocosRoutesGeoOsmhistoryAdmin(OSMGeoAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    verbose_name = "OSM History Rail Routes"

class LocationsAdmin(OSMGeoAdmin):
    list_display = ['wikiname', 'wikislug']
    search_fields = ['wikiname']
    ordering = ['wikiname']
    verbose_name = "Railway Stations from Wikipedia/Naptan"
    formfield_overrides = {models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30},)},}

class RouteLocationAdmin(OSMGeoAdmin):
    list_display = ['routemap_fk', 'loc_no', 'label', 'location_fk']
    search_fields = ['label']
    ordering = ['routemap_fk', 'loc_no']

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

class LocoClassListAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

class LocomotiveAdmin(admin.ModelAdmin):
    list_display = ["brd_number_as_built", "brd_class_name", "brd_build_date_datetime", 'brd_company_grouping_code', 'brd_company_pregrouping_code', ]
    list_filter = ['brd_build_date_datetime', 'brd_company_grouping_code', 'brd_company_pregrouping_code', 'brd_builder']
    search_fields = ("brd_number_as_built", "brd_class_name")
    ordering = ("brd_class_name", 'brd_company_grouping_code', 'brd_company_pregrouping_code',  "brd_number_as_built")

class BuilderAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "pre_grouping_owner", "grouping_owner", "date_opened", "date_closed", "railuk_builder_code", "railuk_builder_code", ]
    search_fields = ["name"]
    ordering = ["name"]

class RouteAdmin(admin.ModelAdmin):
    list_display = ["name", "wikipedia_slug"]
    search_fields = ["name"]
    ordering = ["name"]

class RouteMapAdmin(admin.ModelAdmin):
    list_display = ["name"]
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
admin.site.register(RouteLocation, RouteLocationAdmin)
admin.site.register(RouteMap, RouteMapAdmin)
admin.site.register(ClassBuilder, ClassBuilderAdmin)
admin.site.register(LocoSighting)
admin.site.register(LocoClassSighting)
admin.site.register(LocoClassImage)
admin.site.register(LocoClassList, LocoClassListAdmin)
admin.site.register(SlideHeader)
admin.site.register(Slide, SlideAdmin)
admin.site.register(Slidepack, SlidepackAdmin)
admin.site.register(Locations, LocationsAdmin)
