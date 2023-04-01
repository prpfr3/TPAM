from django.db import models
from .models import *
from notes.models import Post

class Role(models.Model): 
  role = models.CharField(max_length=100, null=True)
  
  def __str__(self):
    return self.role
  
  class Meta:
    managed = True

class Person(models.Model):

  SOURCE_TYPE = (
    (1, 'Wikipedia'),
    (2, 'Custom'),
    )

  """Railway Engineers etc"""
  name = models.CharField(max_length=100, blank=True, default='')
  firstname = models.CharField(max_length=100, default=None)
  surname = models.CharField(max_length=100, default=None) 
  birthdate = models.CharField(max_length=10, blank=True, default='')
  birthplace = models.CharField(max_length=200, blank=True, default='')
  dieddate = models.CharField(max_length=10, blank=True, default='')
  diedplace = models.CharField(max_length=200, blank=True, default='')
  nationality = models.CharField(max_length=200, blank=True, default='') 
  occupation = models.CharField(max_length=200, blank=True, default='')
  wikitextslug = models.CharField(max_length=200, blank=True, default='') 
  wikiimageslug = models.CharField(max_length=200, blank=True, default='')
  wikiimagetext = models.CharField(max_length=200, blank=True, default='')  
  gracetextslug = models.CharField(max_length=200, blank=True, default='') 
  role = models.ManyToManyField(Role, blank=True)
  post_fk = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True, default=None)
  source = models.IntegerField(choices=SOURCE_TYPE, default=1,)
  date_added = models.DateTimeField(auto_now_add=True)
  # lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="person_designer")
  # lococlass_built = models.ManyToManyField(LocoClass, through='ClassManufacturer', related_name="person_manufacturer")
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'People'



