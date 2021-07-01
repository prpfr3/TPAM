from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

class UkAdminBoundaries(models.Model):
    objectid = models.BigIntegerField(blank=True, null=True)
    ctyua19cd = models.CharField(max_length=100,blank=True, null=True)
    ctyua19nm = models.CharField(max_length=100,blank=True, null=True)
    ctyua19nmw = models.CharField(max_length=100,blank=True, null=True)
    bng_e = models.BigIntegerField(blank=True, null=True)
    bng_n = models.BigIntegerField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    st_areasha = models.FloatField(blank=True, null=True)
    st_lengths = models.FloatField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'UK_admin_boundaries'

    def __str__(self):
        return self.ctyua19nm

class GdUkAlwaysOpenLand(models.Model):
    objectid = models.BigIntegerField(db_column='OBJECTID', blank=True, null=True)
    AOL_id = models.FloatField(db_column='AOL_ID', blank=True, null=True)
    name = models.CharField(max_length=100,db_column='Name', blank=True, null=True)
    lastupdate = models.FloatField(db_column='LastUpdate', blank=True, null=True)
    shape_are = models.FloatField(db_column='Shape__Are', blank=True, null=True)
    shape_len = models.FloatField(db_column='Shape__Len', blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gd_UK_always_open_land'
        verbose_name_plural = 'AlwaysOpenedLand'

    def __str__(self):
        return self.name

class GdUkListedBuildings(models.Model):
    listentry = models.BigIntegerField(db_column='ListEntry', blank=True, null=True)
    name = models.CharField(max_length=100,db_column='Name', blank=True, null=True)
    location = models.CharField(max_length=100,db_column='Location', blank=True, null=True)
    grade = models.CharField(max_length=5,db_column='Grade', blank=True, null=True)
    listdate = models.CharField(max_length=20,db_column='ListDate', blank=True, null=True)
    amenddate = models.CharField(max_length=20,db_column='AmendDate', blank=True, null=True)
    legacyuid = models.CharField(max_length=10,db_column='LegacyUID', blank=True, null=True)
    ngr = models.CharField(max_length=20,db_column='NGR', blank=True, null=True)
    capturesca = models.CharField(max_length=10,db_column='CaptureSca', blank=True, null=True)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)
    northing = models.FloatField(db_column='Northing', blank=True, null=True)
    hyperlink = models.URLField(db_column='Hyperlink', blank=True, null=True, max_length=300)
    geometry = models.GeometryField(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gd_UK_listed_buildings'
        verbose_name_plural = 'ListedBuildings'

    def __str__(self):
        return self.name

class GdUkParksGardens(models.Model):
    listentry = models.BigIntegerField(db_column='ListEntry', blank=True, null=True)
    name = models.CharField(max_length=100,db_column='Name', blank=True, null=True)
    grade = models.CharField(max_length=5,db_column='Grade', blank=True, null=True)
    regdate = models.CharField(max_length=20,db_column='RegDate', blank=True, null=True)
    amenddate = models.CharField(max_length=20,db_column='AmendDate', blank=True, null=True)
    legacyuid = models.CharField(max_length=10,db_column='LegacyUID', blank=True, null=True)
    ngr = models.CharField(max_length=20,db_column='NGR', blank=True, null=True)
    capturesca = models.CharField(max_length=10,db_column='CaptureSca', blank=True, null=True)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)
    northing = models.FloatField(db_column='Northing', blank=True, null=True)
    area_ha = models.FloatField(db_column='AREA_HA', blank=True, null=True)
    hyperlink = models.URLField(db_column='Hyperlink', blank=True, null=True, max_length=300)
    geometry = models.GeometryField(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gd_UK_parks_gardens'
        verbose_name_plural = 'Parks & Gardens'

    def __str__(self):
        return self.name

class GdUkScheduledMonuments(models.Model):
    listentry = models.BigIntegerField(db_column='ListEntry', blank=True, null=True)
    name = models.CharField(max_length=100,db_column='Name', blank=True, null=True)
    scheddate = models.CharField(max_length=20,db_column='SchedDate', blank=True, null=True)
    amenddate = models.CharField(max_length=20,db_column='AmendDate', blank=True, null=True)
    legacyuid = models.CharField(max_length=10,db_column='LegacyUID', blank=True, null=True)
    ngr = models.CharField(max_length=20,db_column='NGR', blank=True, null=True)
    capturesca = models.CharField(max_length=10,db_column='CaptureSca', blank=True, null=True)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)
    northing = models.FloatField(db_column='Northing', blank=True, null=True)
    area_ha = models.FloatField(db_column='AREA_HA', blank=True, null=True)
    hyperlink = models.URLField(db_column='Hyperlink', blank=True, null=True, max_length=300)
    geometry = models.GeometryField(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gd_UK_scheduled_monuments'
        verbose_name_plural = 'Scheduled Monuments'

    def __str__(self):
        return self.name

class GdUkWorldHeritageSites(models.Model):
    listentry = models.BigIntegerField(db_column='ListEntry', blank=True, null=True)
    name = models.CharField(max_length=100,db_column='Name', blank=True, null=True)
    inscrdate = models.CharField(max_length=20,db_column='InscrDate', blank=True, null=True)
    amenddate = models.CharField(max_length=20,db_column='AmendDate', blank=True, null=True)
    legacyuid = models.CharField(max_length=10,db_column='LegacyUID', blank=True, null=True)
    notes = models.CharField(max_length=300,db_column='Notes', blank=True, null=True)
    ngr = models.CharField(max_length=20,db_column='NGR', blank=True, null=True)
    capturesca = models.CharField(max_length=10,db_column='CaptureSca', blank=True, null=True)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)
    northing = models.FloatField(db_column='Northing', blank=True, null=True)
    area_ha = models.FloatField(db_column='AREA_HA', blank=True, null=True)
    hyperlink = models.URLField(db_column='Hyperlink', blank=True, null=True, max_length=300)
    geometry = models.GeometryField(blank=True, null=True)
    wikislug = models.SlugField(default=None, blank=True, null=True)
    mynotes = models.TextField(default=None, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gd_UK_world_heritage_sites'
        verbose_name_plural = 'World Heritage Sites'

    def __str__(self):
        return self.name

class Topic(models.Model):
  type = models.ForeignKey('mainmenu.MyDjangoApp', default=1, verbose_name="Topic Type", on_delete=models.SET_DEFAULT)
  text = models.CharField(max_length=25, verbose_name="Topic Name")
  date_added = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(User, on_delete=models.PROTECT)
  def __str__(self):
    return self.text

#This custom object manager allows a different queryset to be used than the standard "all" objects.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))

    title = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    url = models.URLField(default=None, null=True, blank=True)
    slug = models.SlugField(default=None, null=True, blank=True, max_length=255)
    body = models.TextField() 
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    #The first model manager below will be the default. As an additional 'published' manager is specified we have to explicitly define the 'objects' manager as well which would normally be created automatically
    objects = models.Manager() # The model default manager which retrieves all objects
    published = PublishedManager() # Our model custom manager which retrieves only published.

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-publish',) #default sort will be descending on publish

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        if len(self.title) > 50:
            return self.title[:50] + "..." 
        else:
            return self.title

    #Returns a canonical url which is the main url to be used for a specific post
    def get_absolute_url(self):
        return reverse('maps:post_update',
            args=[self.id])

class HeritageSite(models.Model): 
  type = models.ForeignKey('mainmenu.MyDjangoApp', default=1, verbose_name="Heritage Site Type", on_delete=models.SET_DEFAULT)
  site_name = models.CharField(max_length=100, default=None)
  wikislug = models.SlugField(default=None, null=True, max_length=255)
  url = models.URLField(default=None, null=True)
  notes = models.TextField(default=None, null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.site_name

class Visit(models.Model): #Visit to a Location / Heritage Site
  location = models.ForeignKey(HeritageSite, default=1, verbose_name="Location", on_delete=models.SET_DEFAULT)
  date = models.DateField()
  notes = models.TextField(default=None)
  date_added = models.DateField(auto_now_add=True)
  def __str__(self):
    return self.location.site_name 
