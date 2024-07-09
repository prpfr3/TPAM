from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

if settings.GDAL_INSTALLED:
    from django.contrib.gis.db.models import GeometryField

    geometry_fieldtype = GeometryField
else:
    geometry_fieldtype = models.TextField

# class UkAdminBoundaries(models.Model):
#     objectid = models.BigIntegerField(blank=True, null=True)
#     ctyua19cd = models.CharField(max_length=100,blank=True, null=True)
#     ctyua19nm = models.CharField(max_length=100,blank=True, null=True)
#     ctyua19nmw = models.CharField(max_length=100,blank=True, null=True)
#     bng_e = models.BigIntegerField(blank=True, null=True)
#     bng_n = models.BigIntegerField(blank=True, null=True)
#     long = models.FloatField(blank=True, null=True)
#     lat = models.FloatField(blank=True, null=True)
#     st_areasha = models.FloatField(blank=True, null=True)
#     st_lengths = models.FloatField(blank=True, null=True)
#     geometry = geometry_fieldtype(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'UK_admin_boundaries'
#         verbose_name_plural = 'UK Admin Boundaries'

#     def __str__(self):
#         return self.ctyua19nm


class GdUkAlwaysOpenLand(models.Model):
    objectid = models.BigIntegerField(db_column="OBJECTID", blank=True, null=True)
    AOL_id = models.FloatField(db_column="AOL_ID", blank=True, null=True)
    name = models.CharField(max_length=100, db_column="Name", blank=True, null=True)
    lastupdate = models.FloatField(db_column="LastUpdate", blank=True, null=True)
    shape_are = models.FloatField(db_column="Shape__Are", blank=True, null=True)
    shape_len = models.FloatField(db_column="Shape__Len", blank=True, null=True)
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = "gd_UK_always_open_land"
        verbose_name_plural = "AlwaysOpenedLand"

    def __str__(self):
        return self.name


class GdUkListedBuildings(models.Model):
    listentry = models.BigIntegerField(db_column="ListEntry", blank=True, null=True)
    name = models.CharField(max_length=100, db_column="Name", blank=True, null=True)
    location = models.CharField(
        max_length=100, db_column="Location", blank=True, null=True
    )
    grade = models.CharField(max_length=5, db_column="Grade", blank=True, null=True)
    listdate = models.CharField(
        max_length=20, db_column="ListDate", blank=True, null=True
    )
    amenddate = models.CharField(
        max_length=20, db_column="AmendDate", blank=True, null=True
    )
    legacyuid = models.CharField(
        max_length=10, db_column="LegacyUID", blank=True, null=True
    )
    ngr = models.CharField(max_length=20, db_column="NGR", blank=True, null=True)
    capturesca = models.CharField(
        max_length=12, db_column="CaptureSca", blank=True, null=True
    )
    easting = models.FloatField(db_column="Easting", blank=True, null=True)
    northing = models.FloatField(db_column="Northing", blank=True, null=True)
    hyperlink = models.URLField(
        db_column="Hyperlink", blank=True, null=True, max_length=300
    )
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)
    liked = models.ManyToManyField(User, blank=True)  # Used for the Like functionality

    class Meta:
        db_table = "gd_UK_listed_buildings"
        verbose_name_plural = "ListedBuildings"

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        return self.liked.all().count()


class GdUkParksGardens(models.Model):
    listentry = models.BigIntegerField(db_column="ListEntry", blank=True, null=True)
    name = models.CharField(max_length=200, db_column="Name", blank=True, null=True)
    grade = models.CharField(max_length=5, db_column="Grade", blank=True, null=True)
    regdate = models.CharField(
        max_length=20, db_column="RegDate", blank=True, null=True
    )
    amenddate = models.CharField(
        max_length=20, db_column="AmendDate", blank=True, null=True
    )
    legacyuid = models.CharField(
        max_length=10, db_column="LegacyUID", blank=True, null=True
    )
    ngr = models.CharField(max_length=20, db_column="NGR", blank=True, null=True)
    capturesca = models.CharField(
        max_length=15, db_column="CaptureSca", blank=True, null=True
    )
    easting = models.FloatField(db_column="Easting", blank=True, null=True)
    northing = models.FloatField(db_column="Northing", blank=True, null=True)
    area_ha = models.FloatField(db_column="AREA_HA", blank=True, null=True)
    hyperlink = models.URLField(
        db_column="Hyperlink", blank=True, null=True, max_length=300
    )
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = "gd_UK_parks_gardens"
        verbose_name_plural = "Parks & Gardens"

    def __str__(self):
        return self.name


class GdUkScheduledMonuments(models.Model):
    listentry = models.BigIntegerField(db_column="ListEntry", blank=True, null=True)
    name = models.CharField(max_length=100, db_column="Name", blank=True, null=True)
    scheddate = models.CharField(
        max_length=20, db_column="SchedDate", blank=True, null=True
    )
    amenddate = models.CharField(
        max_length=20, db_column="AmendDate", blank=True, null=True
    )
    legacyuid = models.CharField(
        max_length=10, db_column="LegacyUID", blank=True, null=True
    )
    ngr = models.CharField(max_length=20, db_column="NGR", blank=True, null=True)
    capturesca = models.CharField(
        max_length=15, db_column="CaptureSca", blank=True, null=True
    )
    easting = models.FloatField(db_column="Easting", blank=True, null=True)
    northing = models.FloatField(db_column="Northing", blank=True, null=True)
    area_ha = models.FloatField(db_column="AREA_HA", blank=True, null=True)
    hyperlink = models.URLField(
        db_column="Hyperlink", blank=True, null=True, max_length=300
    )
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = "gd_UK_scheduled_monuments"
        verbose_name_plural = "Scheduled Monuments"

    def __str__(self):
        return self.name


class GdUkWorldHeritageSites(models.Model):
    listentry = models.BigIntegerField(db_column="ListEntry", blank=True, null=True)
    name = models.CharField(max_length=100, db_column="Name", blank=True, null=True)
    inscrdate = models.CharField(
        max_length=20, db_column="InscrDate", blank=True, null=True
    )
    amenddate = models.CharField(
        max_length=20, db_column="AmendDate", blank=True, null=True
    )
    legacyuid = models.CharField(
        max_length=10, db_column="LegacyUID", blank=True, null=True
    )
    notes = models.CharField(max_length=300, db_column="Notes", blank=True, null=True)
    ngr = models.CharField(max_length=20, db_column="NGR", blank=True, null=True)
    capturesca = models.CharField(
        max_length=10, db_column="CaptureSca", blank=True, null=True
    )
    easting = models.FloatField(db_column="Easting", blank=True, null=True)
    northing = models.FloatField(db_column="Northing", blank=True, null=True)
    area_ha = models.FloatField(db_column="AREA_HA", blank=True, null=True)
    hyperlink = models.URLField(
        db_column="Hyperlink", blank=True, null=True, max_length=300
    )
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        db_table = "gd_UK_world_heritage_sites"
        verbose_name_plural = "World Heritage Sites"

    def __str__(self):
        return self.name


class MyPlaces(models.Model):
    name = models.CharField(max_length=100, db_column="Name", blank=True, null=True)
    easting = models.FloatField(db_column="Easting", blank=True, null=True)
    northing = models.FloatField(db_column="Northing", blank=True, null=True)
    hyperlink = models.URLField(
        db_column="Hyperlink", blank=True, null=True, max_length=300
    )
    geometry = geometry_fieldtype(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)
    favourite = models.ManyToManyField(
        User, blank=True
    )  # Used for the Like functionality
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="myplace_owner", on_delete=models.CASCADE
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "MyPlaces"

    def __str__(self):
        return self.name

    @property
    def like_count(self):
        return self.favourite.all().count()
