from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

class PersonAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "birthdate", "dieddate", "wikitextslug",]
    ordering = ('name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role",]
    ordering = ('role',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

admin.site.register(Person,PersonAdmin)
admin.site.register(Role,RoleAdmin)