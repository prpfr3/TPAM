from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
# GeoModelAdmin is an alternative to OSMGeoAdmin which provides less map detail
from .models import Shop, GdUkListedBuildings, GdUkAlwaysOpenLand, GdUkParksGardens, GdUkScheduledMonuments, UkAdminBoundaries, Topic, Post, HeritageSite, Visit
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

@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
    verbose_name = 'Shops'

@admin.register(UkAdminBoundaries)
class UkAdminBoundariesAdmin(OSMGeoAdmin):
    list_display = ['ctyua19cd', 'ctyua19nm']
    search_fields = ['ctyua19nm']
    ordering = ['ctyua19nm']
    verbose_name = "UK Administrative Boundaries"

@admin.register(GdUkAlwaysOpenLand)
class GdUkAlwaysOpenLandAdmin(OSMGeoAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    verbose_name = "UK National Trust Always Open Land Area"

@admin.register(GdUkParksGardens)
class GdUkParksGardensAdmin(OSMGeoAdmin):
    list_display = ['listentry', 'name']
    search_fields = ['name']
    ordering = ['name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    verbose_name = "Historic England Parks and Gardens Listing"

@admin.register(GdUkScheduledMonuments)
class GdUkScheduledMonumentsAdmin(OSMGeoAdmin):
    list_display = ['listentry', 'name']
    search_fields = ['name']
    ordering = ['name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    verbose_name = "Historic England Scheduled Monuments Listings"

@admin.register(GdUkListedBuildings)
class GdUkListedBuildingsAdmin(OSMGeoAdmin):
    list_display = ('listentry', 'name', 'location', 'grade')
    search_fields = ['name', 'location']
    list_filter = ['grade']
    ordering = ['name']
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}
    verbose_name = "Historic England Listed Buildings"

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