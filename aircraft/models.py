from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

class AircraftClass(models.Model): 
  airclass = models.CharField(max_length=100, default=None, blank=True, null=True)
  wikislug = models.SlugField(max_length=250, allow_unicode=True ,default=None, blank=True, null=True)
  description = models.CharField(max_length=500, default=None, blank=True, null=True)
  notes = models.TextField(default=None, blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.description
  class Meta:
    verbose_name_plural = 'Aircraft Classes'
    managed = True


class AirImage(models.Model): #Aircraft Images
  image_name = models.CharField(max_length=100, default=None)
  image = models.ImageField(upload_to='images/')
  airclass = models.ForeignKey(AircraftClass, default=1, verbose_name="Aircraft Class", on_delete=models.SET_DEFAULT)
  location = models.ForeignKey('locations.HeritageSite', default=1, verbose_name="Location", on_delete=models.SET_DEFAULT)
  visit = models.ForeignKey('locations.Visit', default=1, verbose_name="Visit", on_delete=models.SET_DEFAULT)
  notes = models.TextField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.image_name

class AirBMImage(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='airimages_created',
                            on_delete=models.CASCADE) #Ensures table entries here are deleted when the user is deleted
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200,
                          blank=True)
  url = models.URLField()
  image = models.ImageField(upload_to='images/%Y/%m/%d/')
  description = models.TextField(blank=True)
  created = models.DateField(auto_now_add=True,
                              db_index=True)
  #Related name has to be changed to prevent a clash with the matching code for model MVBMImage
  users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='airimages_liked',
                                  blank=True)

  def __str__(self):
      return self.title