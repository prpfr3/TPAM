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
        "get_post_fk",
    ]
    ordering = ("name",)
    search_fields = ("name", "post_fk__title")
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
    raw_id_fields = ["post_fk"]
    filter_horizontal = ["references"]
    inlines = [RoleInline]

    def get_post_fk(self, obj):
        return obj.post_fk.title if obj.post_fk is not None else None

    get_post_fk.short_description = "Post FK"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "post_fk":
            kwargs["queryset"] = Post.objects.all().order_by("title")
            kwargs["widget"] = ForeignKeyRawIdWidget(
                db_field.remote_field, self.admin_site
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
    # filter_horizontal = ["persons"]


class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ["person", "role", "date_from", "date_to"]
    ordering = ("person",)
    search_fields = ["person__name", "role__role"]
    raw_id_fields = ["person", "role"]


admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(PersonRole, PersonRoleAdmin)
