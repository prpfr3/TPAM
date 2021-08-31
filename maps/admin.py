from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
# GeoModelAdmin is an alternative to OSMGeoAdmin which provides less map detail
from .models import Topic, Post, HeritageSite, Visit
from datetime import datetime
from django.contrib.gis.db import models
from tinymce.widgets import TinyMCE

@admin.register(HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):
    list_display = ["id", "site_name", "wikislug", "url"]
    ordering = ('site_name',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "date", "notes"]
    ordering = ('date',)
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "topic", "owner", "publish", "status"]
    list_filter = ["status", "created", "publish", "owner"]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('owner',) # Creates a lookup widget for large volume lookups
    date_hierarchy = 'publish'
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

admin.site.register(Topic)