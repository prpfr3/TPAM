from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class HeritageSite(models.Model): 
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

class MilitaryVehicleClass(models.Model): 
  mvclass = models.CharField(max_length=100, default=None, blank=True, null=True)
  wikislug = models.SlugField(max_length=250, default=None, blank=True, null=True)
  description = models.CharField(max_length=500, default=None, blank=True, null=True)
  notes = models.TextField(default=None, blank=True, null=True)
  favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav',
    related_name='favorite_things')
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.description

  class Meta:
    verbose_name_plural = 'Military Vehicle Classes'
    managed = True

class Fav(models.Model) :
    thing = models.ForeignKey(MilitaryVehicleClass, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='favs_users')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('thing', 'user')

    def __str__(self):
      return f'{self.user.username} likes {self.thing.mvclass[:10]}'


class MVImage(models.Model): #Military Vehicle Images
  image_name = models.CharField(max_length=100, default=None)
  image = models.ImageField(upload_to='images/')
  mvclass = models.ForeignKey(MilitaryVehicleClass, default=1, verbose_name="Military Vehicle Class", on_delete=models.SET_DEFAULT)
  location = models.ForeignKey(HeritageSite, default=1, verbose_name="Location", on_delete=models.SET_DEFAULT)
  visit = models.ForeignKey(Visit, default=1, verbose_name="Visit", on_delete=models.SET_DEFAULT)
  notes = models.TextField(default=None, blank=True, null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.image_name


class MVBMImage(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='mvimages_created',on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200, blank=True)
  url = models.URLField()
  image = models.ImageField(upload_to='images/%Y/%m/%d/')
  description = models.TextField(blank=True)
  created = models.DateField(auto_now_add=True, db_index=True)
  users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='mvimages_liked',# Needed because of similar relationships in other appas
                                  blank=True)

  def __str__(self):
      return self.title