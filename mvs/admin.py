from django.contrib import admin
from mvs.models import *
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models


class MVBMImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']


class MilitaryVehicleClassAdmin(admin.ModelAdmin):
    list_display = ["id", "mvclass", "description", "wikislug"]
    search_fields = ['mvclass', 'description']
    ordering = ('mvclass',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()}, }


class MVImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'image',
                    'mvclass', 'location', 'notes', 'date_added']
    search_fields = ['image_name', 'mvclass__mvclass']
    ordering = ('image_name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()}, }


admin.site.register(MVBMImage, MVBMImageAdmin)
admin.site.register(MVImage, MVImageAdmin)
admin.site.register(MilitaryVehicleClass, MilitaryVehicleClassAdmin)
admin.site.register(Visit)
admin.site.register(HeritageSite)
