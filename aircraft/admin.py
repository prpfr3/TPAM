from django.contrib import admin
from aircraft.models import AircraftClass, AirImage, AirBMImage
from datetime import datetime
from tinymce.widgets import TinyMCE
from django.db import models

class AirBMImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']

class AircraftClassAdmin(admin.ModelAdmin):
    list_display = ["id", "airclass", "description", "wikislug"]
    ordering = ('airclass',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class AirImageAdmin(admin.ModelAdmin):
    list_display = ['image_name', 'image', 'airclass', 'location', 'notes', 'date_added']
    ordering = ('image_name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

admin.site.register(AirBMImage, AirBMImageAdmin)
admin.site.register(AirImage, AirImageAdmin)
admin.site.register(AircraftClass, AircraftClassAdmin)