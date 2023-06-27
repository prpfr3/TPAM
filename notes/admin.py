from django.contrib import admin
from .models import *
from django.db import models
from tinymce.widgets import TinyMCE


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "topic", "owner", "publish", "status"]
    list_filter = ["status", "created", "publish", "owner"]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    # Creates a lookup widget for large volume lookups
    raw_id_fields = ('owner',)
    date_hierarchy = 'publish'
    formfield_overrides = {models.TextField: {'widget': TinyMCE()}, }
    # Add this line to enable a search box for the references field
    filter_horizontal = ['references']


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ['full_reference', 'image']
    list_filter = ["type"]


admin.site.register(Topic)
