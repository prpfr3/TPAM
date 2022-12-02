from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey



class VehicleType(models.Model): 
  type = models.CharField(max_length=25, null=True)
  def __str__(self):
    return self.type
  class Meta:
    verbose_name_plural = 'Vehicle Types'
    managed = True


class VehicleMake(models.Model): 
  make = models.CharField(max_length=50)
  date_added = models.DateTimeField(auto_now_add=True)
  type = models.ForeignKey(VehicleType, default=None, verbose_name="Vehicle Type", on_delete=models.SET_DEFAULT)
  def __str__(self):
    return self.make
  class Meta:
    verbose_name_plural = 'Vehicle Make'
    managed = True


class VehicleModel(models.Model): 
  model = models.CharField(max_length=80)
  date_added = models.DateTimeField(auto_now_add=True)
  make = models.ForeignKey(VehicleMake, default=None, verbose_name="Vehicle Make", on_delete=models.SET_DEFAULT)

  def __str__(self):
    return self.model
  class Meta:
    verbose_name_plural = 'Vehicle Models'
    managed = True


class VehicleVariant(models.Model): 
  variant = models.CharField(max_length=80)
  date_added = models.DateTimeField(auto_now_add=True)
  model = models.ForeignKey(VehicleModel, default=None, verbose_name="Vehicle Model", on_delete=models.SET_DEFAULT)
  def __str__(self):
    return self.variant
  class Meta:
    verbose_name_plural = 'Vehicle Variants'
    managed = True

"""
ChainedForeignKey solution based on https://github.com/jazzband/django-smart-selects/issues/292

"""
class UKLicensedVehicles(models.Model):
  year_ending = models.PositiveIntegerField(default='2020')
  type = models.ForeignKey(VehicleType, default=None, null=True, verbose_name="Vehicle Type", on_delete=models.SET_DEFAULT)#Added for smart selects
  make = ChainedForeignKey(
      VehicleMake, 
      default=None,
      null=True,
      chained_field="type",
      chained_model_field="type",
      show_all=False,
      auto_choose=True,
      sort=True)
  model = ChainedForeignKey(
      VehicleModel,
      default=None,
      null=True,
      blank=True, #Allows field to be blank on form selection screen
      chained_field="make",
      chained_model_field="make",
      show_all=False,
      auto_choose=True,
      sort=True)
  variant = ChainedForeignKey(
      VehicleVariant, 
      default=None,
      null=True,
      blank=True, #Allows field to be blank on form selection screen
      chained_field="model",
      chained_model_field="model",
      show_all=False,
      auto_choose=True,
      sort=True)
  year_licensed = models.CharField(max_length=30, default=None)
  number_licensed = models.PositiveIntegerField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.variant.variant
  class Meta:
    verbose_name_plural = 'UK Licensed Vehicles'
    managed = True


class VehicleImage(models.Model): #Road Vehicle Images
  image_name = models.CharField(max_length=100, default=None)
  image = models.ImageField(upload_to='images/')
  make = models.ForeignKey(VehicleMake, default=None, verbose_name="Vehicle Make", on_delete=models.SET_DEFAULT)
  model = models.ForeignKey(VehicleModel, default=None, verbose_name="Vehicle Model", on_delete=models.SET_DEFAULT)
  location = models.ForeignKey('maps.HeritageSite', default=None, verbose_name="Location", on_delete=models.SET_DEFAULT)
  visit = models.ForeignKey('maps.Visit', default=None, verbose_name="Visit", on_delete=models.SET_DEFAULT)
  notes = models.TextField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.image_name


class VehicleBMImage(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rvimages_created', on_delete=models.CASCADE) 
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200, blank=True)
  url = models.URLField()
  image = models.ImageField(upload_to='images/%Y/%m/%d/')
  description = models.TextField(blank=True)
  created = models.DateField(auto_now_add=True, db_index=True)
  users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rvimages_liked', blank=True)

  def __str__(self):
      return self.title