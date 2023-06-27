from django.contrib import admin
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "TPAM Administration"  # Set the custom site header
    site_title = "TPAM Admin"  # Set the custom site title
    index_title = "TPAM Tables Admin"  # Set the custom index title


admin.site.__class__ = CustomAdminSite
