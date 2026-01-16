from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.db import models
from tinymce.widgets import TinyMCE

from .models import *


class RoleInline(admin.TabularInline):  # or StackedInline
    model = (
        PersonRole  # This refers to the intermediate model for ManyToMany relationship
    )
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "birthdate",
        "dieddate",
        "wikitextslug",
    ]
    ordering = ("name",)
    search_fields = ("name",)
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
    autocomplete_fields = ["references", "posts"]
    inlines = [RoleInline]


class PersonInline(admin.TabularInline):  # or StackedInline
    model = (
        Person.roles.through
    )  # This refers to the intermediate model for ManyToMany relationship
    extra = 0


class RoleAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "role",
    ]
    ordering = ("role",)
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    inlines = [PersonInline]
    # autocomplete_fields = ["persons"]


class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ["person", "role", "date_from", "date_to"]
    ordering = ("person",)
    search_fields = ["person__name", "role__role"]
    raw_id_fields = ["person", "role"]


admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(PersonRole, PersonRoleAdmin)
