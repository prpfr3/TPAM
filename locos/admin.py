from django.contrib import admin
from locos.models import *
from tinymce.widgets import TinyMCE
from django.db import models

class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "code", ]
    search_fields = ["name"]
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

class LocoClassAdmin(admin.ModelAdmin):
    list_display = ["wikiname", "brdslug", "wheel_body_type"]
    list_filter = ['br_power_class', 'wheel_body_type']
    search_fields = ['wikiname']
    ordering = ['wikiname']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocoClassListAdmin(admin.ModelAdmin):
    list_display = ['name', 'wikislug', 'brdslug', 'lococlass_fk']
    search_fields = ['name', 'wikislug']
    ordering = ['name']

class LocomotiveAdmin(admin.ModelAdmin):
    list_display = ["identifier", "number_pregrouping", "number_grouping", "number_postgrouping"]
    list_filter = ['company_pregrouping_code', 'company_grouping_code', 'builder']
    search_fields = ("identifier", "number_pregrouping", "number_grouping", "number_postgrouping")
    ordering = ("identifier",)

class BuilderAdmin(admin.ModelAdmin):
    list_display = ["name", "wikislug", "pre_grouping_owner", "grouping_owner", "date_opened", "date_closed", "railuk_builder_code", "railuk_builder_code", ]
    search_fields = ["name"]
    ordering = ["name"]

class ClassBuilderAdmin(admin.ModelAdmin):
    list_display = ["lococlass_fk", "builder_fk", "person_fk", "company_fk", ]
    ordering = ["lococlass_fk"]

class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ('whyte_notation', )

# class ReferenceAdmin(admin.ModelAdmin):
#     list_display = ['type', 'citation', 'route_fk', 'ELR_fk', 'location_fk']
#     list_filter = ['type']
#     ordering = ['type', 'citation']
#     search_fields = ['citation']

class SlidepackAdmin(admin.ModelAdmin):
    raw_id_fields = ('slideheader_fk',)
    autocomplete_fields = ['slide_fk']

class SlideAdmin(admin.ModelAdmin):
    ordering = ['text_headline']
    search_fields = ['text_headline']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(PersonRole,PersonRoleAdmin)
admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(Builder, BuilderAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)
admin.site.register(Reference)
admin.site.register(ClassDesigner)
admin.site.register(ClassBuilder, ClassBuilderAdmin)
admin.site.register(LocoClassSighting)
admin.site.register(LocoClassList, LocoClassListAdmin)
# admin.site.register(SlideHeader)
# admin.site.register(Slide, SlideAdmin)
# admin.site.register(Slidepack, SlidepackAdmin)