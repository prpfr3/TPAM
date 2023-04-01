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
    raw_id_fields = ('owner',) # Creates a lookup widget for large volume lookups
    date_hierarchy = 'publish'
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': TinyMCE()},}

admin.site.register(Topic)