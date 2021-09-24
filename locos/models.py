from django.db import models
from django.contrib.auth.models import User

# N.B. Classes have to be listed in order such that a class refering to another appears later in the list

class Depots(models.Model):
    depot = models.CharField(max_length=500, blank=True, null=True)
    codes = models.CharField(max_length=100, blank=True, null=True)
    code_dates = models.CharField(max_length=100, blank=True, null=True)
    date_opened = models.CharField(max_length=20, blank=True, null=True)
    date_closed_to_steam = models.CharField(max_length=20, blank=True, null=True)
    date_closed = models.CharField(max_length=20, blank=True, null=True)
    pre_grouping_company = models.CharField(max_length=20, blank=True, null=True)
    grouping_company = models.CharField(max_length=20, blank=True, null=True)
    br_region = models.CharField(db_column='BR_region', max_length=20, blank=True, null=True)
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    comments = models.TextField()
    image = models.ImageField(upload_to='images/', default=None)
    class Meta:
      verbose_name_plural = 'Depots'

class Engineer(models.Model): 
  """Railway Engineers"""
  eng_name = models.CharField(max_length=100, default=None)
  wikislug = models.SlugField(default=None)
  url = models.URLField(default=None)
  notes = models.TextField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    """Return a string representation of the model"""
    return self.eng_name

class HeritageSite(models.Model): 
  site_name = models.CharField(max_length=100, default=None)
  wikislug = models.SlugField(default=None, null=True, max_length=255)
  url = models.URLField(default=None, null=True)
  notes = models.TextField(default=None, null=True)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.site_name


class ModernClass(models.Model):
  class_type = models.CharField(max_length=1, blank=True, default='')  
  modern_class = models.CharField(max_length=100, blank=True, default='')
  modern_class_slug = models.SlugField(default=None, null=True, max_length=255)
  aka_class = models.CharField(max_length=100, blank=True, default='')
  aka_class_slug = models.SlugField(default=None, null=True, max_length=255)
  year_introduced = models.CharField(max_length=100, blank=True, default='')
  manufacturer = models.CharField(max_length=100, blank=True, default='')
  power_unit = models.CharField(max_length=100, blank=True, default='')
  horse_power = models.CharField(max_length=100, blank=True, default='')
  current = models.CharField(max_length=100, blank=True, default='')
  wheel_id = models.CharField(max_length=100, blank=True, default='')
  wheel_id_slug = models.SlugField(default=None, null=True, max_length=255)
  transmission = models.CharField(max_length=50, blank=True, default='')
  number_range = models.CharField(max_length=255, blank=True, default='')
  number_range_slug = models.SlugField(default=None, null=True, max_length=255)
  number_built = models.CharField(max_length=100, blank=True, default='')
  multiple = models.CharField(max_length=100, blank=True, default='')
  img_slug = models.SlugField(default=None, null=True, max_length=255)

  class Meta:
    verbose_name_plural = 'Post Steam Locomotive Classes'
    managed = True
  def __str__(self):
    return self.modern_class



class Manufacturers(models.Model):
  manufacturer_code = models.CharField(max_length=3, blank=True, null=True)
  manufacturer_name = models.CharField(max_length=50, blank=True, null=True)
  location = models.CharField(max_length=200, blank=True, null=True)
  date_opened = models.CharField(max_length=10, blank=True, null=True)
  date_closed = models.CharField(max_length=10, blank=True, null=True)
  type = models.CharField(max_length=77, blank=True, null=True)
  steam = models.CharField(max_length=10, blank=True, null=True)
  diesel = models.CharField(max_length=10, blank=True, null=True)
  electric = models.CharField(max_length=10, blank=True, null=True)
  map = models.CharField(max_length=200, blank=True, null=True)
  web = models.CharField(max_length=200, blank=True, null=True)
  class Meta:
    verbose_name_plural = 'Manufacturers' 

class WheelArrangement(models.Model):
    uic_system = models.CharField(db_column='UIC_system', max_length=20, blank=True, null=True)
    whyte_notation = models.CharField(db_column='Whyte_notation', max_length=20, blank=True, null=True)
    american_name = models.CharField(db_column='American_name', max_length=75, blank=True, null=True)
    visual = models.CharField(db_column='Visual', max_length=20, blank=True, null=True)

class LocoClass(models.Model):
  grouping_company = models.CharField(max_length=10, blank=True, default='')
  pre_grouping_company = models.CharField(max_length=20, blank=True, default='')
  #designer = models.ForeignKey(Engineer, default=1, verbose_name="Designer", on_delete=models.SET_DEFAULT)
  designer = models.CharField(max_length=100, blank=True, default='')
  designer_slug = models.SlugField(null=True, max_length=255)
  grouping_class = models.CharField(max_length=100, blank=True, default='')
  grouping_class_slug = models.SlugField(default=None, null=True, max_length=255)
  pre_grouping_class = models.CharField(max_length=100, blank=True, default='')
  br_power_class = models.CharField(max_length=5, blank=True, default='')
  wheel_body_type = models.CharField(max_length=100, blank=True, default='')
  wheel_arrangement = models.ForeignKey(WheelArrangement, default=None, blank=None, null=True, verbose_name="Wheel Arrangement", on_delete=models.SET_DEFAULT)
  year_built = models.CharField(max_length=100, blank=True, default='')
  number_range = models.CharField(max_length=100, blank=True, default='')
  number_range_slug = models.SlugField(default=None, null=True, max_length=255)
  year_first_built = models.CharField(max_length=100, blank=True, default='')
  year_last_built = models.CharField(max_length=100, blank=True, default='')
  number_built = models.CharField(max_length=100, blank=True, default='')
  img_slug = models.SlugField(default=None, null=True, max_length=255)
  class Meta:
    verbose_name_plural = 'Locomotive Classes'
    managed = True
  def __str__(self):
    return self.grouping_class

class Locomotive(models.Model):
  build_date = models.CharField(max_length=10, blank=True, null=True)
  pre_grouping_class = models.CharField(max_length=10, blank=True, null=True)
  steam_class = models.ForeignKey(LocoClass, default=None, null=True, blank=True, verbose_name="Steam Class", on_delete=models.SET_DEFAULT)
  modern_class = models.ForeignKey(ModernClass, default=None, null=True, blank=True, verbose_name="Modern Class", on_delete=models.SET_DEFAULT)
  number = models.CharField(max_length=20, blank=True, null=True)
  wheel_arrangement = models.CharField(max_length=10, blank=True, null=True)
  designer = models.CharField(max_length=30, blank=True, null=True)
  manufacturer = models.CharField(max_length=50, blank=True, null=True)
  order_number = models.CharField(max_length=30, blank=True, null=True)
  works_number = models.CharField(max_length=30, blank=True, null=True)
  withdrawn = models.CharField(max_length=15, blank=True, null=True)
  images = models.ManyToManyField('Image', through='HeritageLocoSeen')

  def __str__(self):
    return self.number

class Visit(models.Model): #Visit to a Location / Heritage Site
  location = models.ForeignKey(HeritageSite, default=1, verbose_name="Location", on_delete=models.SET_DEFAULT)
  date = models.DateField()
  notes = models.TextField(default=None)
  date_added = models.DateField(auto_now_add=True)
  def __str__(self):
    return self.location.site_name

class Image(models.Model): #Railway Images
  image_name = models.CharField(max_length=100, default=None)
  image = models.ImageField(upload_to='images/')
  loco_class = models.ForeignKey(LocoClass, default=1, verbose_name="Locomotive Class", on_delete=models.SET_DEFAULT)
  locos = models.ManyToManyField('Locomotive', through='HeritageLocoSeen')
  location = models.ForeignKey('maps.HeritageSite', default=1, verbose_name="Location", on_delete=models.SET_DEFAULT)
  visit = models.ForeignKey('maps.Visit', default=1, verbose_name="Visit", on_delete=models.SET_DEFAULT)
  notes = models.TextField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.image_name

class HeritageLocoSeen(models.Model): #Specifies loco seen in an image
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    loco = models.ForeignKey(Locomotive, on_delete=models.CASCADE)

    INSTEAM = 1
    OUTOFSERVICE = 2

    LOCO_STATUS = (
        ( INSTEAM, 'In Steam'),
        ( OUTOFSERVICE, 'Out of Service'),
    )

    loco_status = models.IntegerField(
        choices=LOCO_STATUS,
        default=INSTEAM,
        )

    def __str__(self):
        return "Image "+ str(self.image.id) + " of Loco " + str(self.loco.number)