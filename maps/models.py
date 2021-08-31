from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_owner')
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
