from django.contrib import admin
from locos.models import PersonRole, Role, Depots, Person, Image, ModernClass, Locomotive, Manufacturers, WheelArrangement, LocoClass
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

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

class PersonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "wikislug",]
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
    list_display = ["grouping_company", "pre_grouping_company", "grouping_class", "pre_grouping_class", "br_power_class", "designer", "wheel_body_type", "year_built", "year_first_built", "year_last_built"]
    list_filter = ['grouping_company', 'pre_grouping_company', 'br_power_class', 'wheel_body_type', 'designer']
    search_fields = ('grouping_class', 'pre_grouping_class')
    ordering = ['grouping_company', 'pre_grouping_company', 'grouping_class']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
 
class ModernClassAdmin(admin.ModelAdmin):
    list_display = ["modern_class", "aka_class", "wheel_id"]
    list_filter = ['transmission', 'manufacturer']
    search_fields = ['modern_class']
    ordering = ['modern_class']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class LocomotiveAdmin(admin.ModelAdmin):
    list_display = ["number", "pre_grouping_class"]
    list_filter = ['pre_grouping_class']
    search_fields = ('pre_grouping_class', 'number')
    ordering = ('pre_grouping_class', 'number')

class ManufacturersAdmin(admin.ModelAdmin):
    list_display = ["manufacturer_code", "manufacturer_name"]
    search_fields = ("manufacturer_code", "manufacturer_name")
    ordering = ("manufacturer_code", "manufacturer_name")

class WheelArrangementAdmin(admin.ModelAdmin):
    list_display = ["whyte_notation", "uic_system", "american_name", "visual"]
    ordering = ('whyte_notation', )

admin.site.register(Depots, DepotsAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(PersonRole,PersonRoleAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(LocoClass, LocoClassAdmin)
admin.site.register(ModernClass, ModernClassAdmin)
admin.site.register(Locomotive, LocomotiveAdmin)
admin.site.register(Manufacturers, ManufacturersAdmin)
admin.site.register(WheelArrangement, WheelArrangementAdmin)