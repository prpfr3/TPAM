from django.contrib.gis.db import models
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
  builder = models.CharField(max_length=100, blank=True, default='')
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



class WheelArrangement(models.Model):
    uic_system = models.CharField(db_column='UIC_system', max_length=20, blank=True, null=True)
    whyte_notation = models.CharField(db_column='Whyte_notation', max_length=20, blank=True, null=True)
    american_name = models.CharField(db_column='American_name', max_length=75, blank=True, null=True)
    visual = models.CharField(db_column='Visual', max_length=20, blank=True, null=True)

class LocoClass(models.Model):
  grouping_company = models.CharField(max_length=10, blank=True, default='')
  pre_grouping_company = models.CharField(max_length=20, blank=True, default='')
  grouping_class = models.CharField(max_length=500, blank=True, default='')
  grouping_class_slug = models.SlugField(default=None, null=True, max_length=255) #1923-1947
  pre_grouping_class = models.CharField(max_length=100, blank=True, default='') #pre1923
  br_power_class = models.CharField(max_length=5, blank=True, default='') #1948-1997
  wheel_body_type = models.CharField(max_length=100, blank=True, default='')
  wheel_arrangement = models.ForeignKey(WheelArrangement, default=None, blank=None, null=True, verbose_name="Wheel Arrangement", on_delete=models.SET_DEFAULT)
  year_built = models.CharField(max_length=100, blank=True, default='')
  number_range = models.CharField(max_length=100, blank=True, default='')
  number_range_slug = models.SlugField(default=None, null=True, max_length=255)
  year_first_built = models.CharField(max_length=100, blank=True, default='')
  year_last_built = models.CharField(max_length=100, blank=True, default='')
  number_built = models.CharField(max_length=100, blank=True, default='')
  img_slug = models.SlugField(default=None, null=True, max_length=255)

  adhesive_weight = models.CharField(max_length=200, blank=True, default='')
  adhesion_factor = models.CharField(max_length=40, blank=True, default='')
  alternator = models.CharField(max_length=75, blank=True, default='') 
  axle_load = models.CharField(max_length=200, blank=True, default='')
  axle_load_class = models.CharField(max_length=200, blank=True, default='')
  bogie = models.CharField(max_length=100, blank=True, default='')
  bogies = models.CharField(max_length=100, blank=True, default='')
  boiler = models.CharField(max_length=200, blank=True, default='')
  boiler_pressure = models.CharField(max_length=200, blank=True, default='')
  boiler_diameter = models.CharField(max_length=200, blank=True, default='')
  boiler_model = models.CharField(max_length=200, blank=True, default='')
  boiler_pitch = models.CharField(max_length=200, blank=True, default='')
  boiler_tube_plates = models.CharField(max_length=200, blank=True, default='')
  brakeforce = models.CharField(max_length=200, blank=True, default='')
  build_date = models.CharField(max_length=200, blank=True, default='')
  coolant_capacity = models.CharField(max_length=50, blank=True, default='')
  couplers = models.CharField(max_length=50, blank=True, default='')
  coupled_diameter = models.CharField(max_length=50, blank=True, default='')
  current_pickups = models.CharField(max_length=300, blank=True, default='')  
  cylinder_size = models.CharField(max_length=300, blank=True, default='')
  cylinders = models.CharField(max_length=125, blank=True, default='')
  displacement = models.CharField(max_length=200, blank=True, default='')
  disposition = models.CharField(max_length=200, blank=True, default='')
  driver_diameter = models.CharField(max_length=200, blank=True, default='')
  electric_systems = models.CharField(max_length=200, blank=True, default='')
  engine_maximum_rpm = models.CharField(max_length=50, blank=True, default='')
  engine_type = models.CharField(max_length=100, blank=True, default='') 
  firegrate_area = models.CharField(max_length=100, blank=True, default='')
  fuel_capacity = models.CharField(max_length=200, blank=True, default='')
  fuel_type = models.CharField(max_length=100, blank=True, default='')
  gauge = models.CharField(max_length=175, blank=True, default='')
  gear_ratio = models.CharField(max_length=100, blank=True, default='')
  generator = models.CharField(max_length=150, blank=True, default='')
  heating_area = models.CharField(max_length=200, blank=True, default='')
  heating_surface = models.CharField(max_length=200, blank=True, default='')
  heating_surface_firebox = models.CharField(max_length=200, blank=True, default='')
  heating_surface_tubes_flues = models.CharField(max_length=200, blank=True, default='')
  heating_surface_tubes = models.CharField(max_length=200, blank=True, default='')
  heating_surface_flues = models.CharField(max_length=200, blank=True, default='')
  height = models.CharField(max_length=200, blank=True, default='')
  height_pantograph = models.CharField(max_length=100, blank=True, default='')
  high_pressure_cylinder = models.CharField(max_length=200, blank=True, default='')
  leading_diameter = models.CharField(max_length=200, blank=True, default='')
  length_over_beams = models.CharField(max_length=200, blank=True, default='')
  length = models.CharField(max_length=200, blank=True, default='')
  loco_brake = models.CharField(max_length=200, blank=True, default='')
  loco_weight = models.CharField(max_length=250, blank=True, default='')
  low_pressure_cylinder = models.CharField(max_length=200, blank=True, default='')
  lubricant_capacity = models.CharField(max_length=100, blank=True, default='')
  model = models.CharField(max_length=100, blank=True, default='')
  maximum_speed = models.CharField(max_length=200, blank=True, default='')
  minimum_curve = models.CharField(max_length=200, blank=True, default='')
  mu_working = models.CharField(max_length=200, blank=True, default='')
  nicknames = models.CharField(max_length=200, blank=True, default='')
  number_in_class = models.CharField(max_length=200, blank=True, default='')
  number_rebuilt = models.CharField(max_length=200, blank=True, default='')
  numbers = models.CharField(max_length=700, blank=True, default='')
  official_name = models.CharField(max_length=200, blank=True, default='')
  order_number = models.CharField(max_length=200, blank=True, default='')
  pivot_centres = models.CharField(max_length=200, blank=True, default='')
  power_class = models.CharField(max_length=200, blank=True, default='')
  power_output = models.CharField(max_length=200, blank=True, default='')
  power_output_one_hour = models.CharField(max_length=200, blank=True, default='')
  power_output_continuous = models.CharField(max_length=200, blank=True, default='')
  power_output_starting = models.CharField(max_length=200, blank=True, default='')
  power_type = models.CharField(max_length=200, blank=True, default='')
  prime_mover = models.CharField(max_length=200, blank=True, default='')
  rebuild_date = models.CharField(max_length=200, blank=True, default='')
  rebuilder = models.CharField(max_length=200, blank=True, default='')
  retired = models.CharField(max_length=200, blank=True, default='')
  rpm_range = models.CharField(max_length=200, blank=True, default='')
  safety_systems = models.CharField(max_length=200, blank=True, default='')
  serial_number = models.CharField(max_length=250, blank=True, default='')
  superheater_type = models.CharField(max_length=200, blank=True, default='')
  tender_capacity = models.CharField(max_length=200, blank=True, default='')
  tender_type = models.CharField(max_length=200, blank=True, default='')
  tender_weight = models.CharField(max_length=300, blank=True, default='')
  total_weight = models.CharField(max_length=200, blank=True, default='')
  tractive_effort = models.CharField(max_length=200, blank=True, default='')
  traction_motors = models.CharField(max_length=200, blank=True, default='')
  trailing_diameter = models.CharField(max_length=200, blank=True, default='')
  train_brakes = models.CharField(max_length=200, blank=True, default='')
  train_heating = models.CharField(max_length=200, blank=True, default='')
  transmission = models.CharField(max_length=200, blank=True, default='')
  UIC = models.CharField(max_length=200, blank=True, default='')
  valve_gear = models.CharField(max_length=200, blank=True, default='')
  valve_type = models.CharField(max_length=200, blank=True, default='')
  water_capacity = models.CharField(max_length=300, blank=True, default='')
  wheel_configuration_aar = models.CharField(max_length=200, blank=True, default='')
  wheel_configuration_commonwealth = models.CharField(max_length=200, blank=True, default='')
  wheelbase = models.CharField(max_length=200, blank=True, default='')
  wheelbase_engine = models.CharField(max_length=200, blank=True, default='')
  wheelbase_tender = models.CharField(max_length=200, blank=True, default='')
  wheel_diameter = models.CharField(max_length=200, blank=True, default='')
  whyte = models.CharField(max_length=200, blank=True, default='')
  width = models.CharField(max_length=200, blank=True, default='')
  withdrawn = models.CharField(max_length=200, blank=True, default='')

  class Meta:
    verbose_name_plural = 'Locomotive Classes'
    managed = True

  def __str__(self):
    return self.grouping_class


class Person(models.Model): 
  """Railway Engineers etc"""
  name = models.CharField(max_length=100, default=None)
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
  notes = models.TextField(default=None)
  date_added = models.DateTimeField(auto_now_add=True)
  # Whereas Company needed a related name for this Many-to-Many, objects Builder and Person did not. All three share the ClassDesigner table
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="person_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="person_builder")
  def __str__(self):
    """Return a string representation of the model"""
    return self.name

class Role(models.Model): 
  role = models.CharField(max_length=100, null=True)
  def __str__(self):
    return self.role
  class Meta:
    managed = True

class PersonRole(models.Model): 
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  person = models.ForeignKey(Person, on_delete=models.CASCADE)

  def __str__(self):
    return "{} {}".format(self.person.name, self.role.role)

class Builder(models.Model):
  name = models.CharField(max_length=200, blank=True, null=True)
  wikislug = models.SlugField(max_length=200, default=None)
  railuk_builder_code = models.CharField(max_length=3, blank=True, null=True)
  brd_builder_code = models.CharField(max_length=3, blank=True, null=True)
  brsl_builder_code = models.CharField(max_length=10, blank=True, null=True)
  location = models.CharField(max_length=200, blank=True, null=True)
  pre_grouping_owner = models.CharField(max_length=10, blank=True, default='') #pre1923
  grouping_owner = models.CharField(max_length=4, blank=True, default='') #1923-1947
  br_region_owner = models.CharField(max_length=3, blank=True, default='') #1948-1997
  date_opened = models.CharField(max_length=10, blank=True, null=True)
  date_closed = models.CharField(max_length=10, blank=True, null=True)
  type = models.CharField(max_length=77, blank=True, null=True)
  steam = models.CharField(max_length=10, blank=True, null=True)
  diesel = models.CharField(max_length=10, blank=True, null=True)
  electric = models.CharField(max_length=10, blank=True, null=True)
  map = models.CharField(max_length=200, blank=True, null=True)
  web = models.CharField(max_length=200, blank=True, null=True)
  # Whereas Company needed a related name for this Many-to-Many, objects Builder and Person did not. All three share the ClassDesigner table
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="builder_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="builder_builder")

    
  class Meta:
    verbose_name_plural = 'Builder' 


class CompanyCategory(models.Model):
  category = models.CharField(max_length=100, null=True)
  def __str__(self):
    return self.category
  class Meta:
    managed = True

class Company(models.Model):
  name = models.CharField(max_length=200, blank=True, null=True)
  wikislug = models.SlugField(max_length=200, default=None)
  code = models.CharField(max_length=10, blank=True, null=True)
  loco_classes = models.ManyToManyField(LocoClass)
  company_categories = models.ManyToManyField(CompanyCategory)
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="company_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="company_builder")
  class Meta:
    verbose_name_plural = 'Companies'

class ClassBuilder(models.Model): 
  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  builder_fk = models.ForeignKey(Builder, blank=True, null=True, on_delete=models.CASCADE)
  person_fk = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

  def __str__(self):
    if self.person_fk != "":
      builder = self.person_fk
    elif self.builder_fk != "":
      builder = self.builder_fk
    elif self.company_fk != "":
      builder = self.company_fk
    return "{}".format(builder)

class ClassDesigner(models.Model): 

  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  builder_fk = models.ForeignKey(Builder, blank=True, null=True, on_delete=models.CASCADE)
  person_fk = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)

  def __str__(self):
    if self.person_fk != "":
      designer_name = self.person_fk
    elif self.builder_fk != "":
      designer_name = self.builder_fk
    elif self.company_fk != "":
      designer_name = self.company_fk
    return "{}".format(designer_name)

class ClassOwnerOperator(models.Model): 
  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, on_delete=models.CASCADE)

  def __str__(self):
    return "{} {}".format(self.lococlass_fk, self.company_fk)

class Locomotive(models.Model):
  build_date = models.CharField(max_length=10, blank=True, null=True)
  pre_grouping_class = models.CharField(max_length=10, blank=True, null=True)
  steam_class = models.ForeignKey(LocoClass, default=None, null=True, blank=True, verbose_name="Steam Class", on_delete=models.SET_DEFAULT)
  modern_class = models.ForeignKey(ModernClass, default=None, null=True, blank=True, verbose_name="Modern Class", on_delete=models.SET_DEFAULT)
  number = models.CharField(max_length=20, blank=True, null=True)
  wheel_arrangement = models.CharField(max_length=10, blank=True, null=True)
  designer = models.CharField(max_length=30, blank=True, null=True)
  builder = models.CharField(max_length=50, blank=True, null=True)
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

class Sighting(models.Model): #Specifies a sighting
    locos = models.ManyToManyField(Locomotive, through='LocoSighting')
    lococlass = models.ManyToManyField(LocoClass, through='LocoClassSighting')

    DD = models.CharField(max_length=2, blank='True', null='True', default=None)
    MM = models.CharField(max_length=2, blank='True', null='True', default=None)
    YD = models.CharField(max_length=1, blank='True', null='True', default=None) #Year decade (for when the year is not accurately known)
    YY = models.CharField(max_length=1, blank='True', null='True', default=None) #Year within the decade
    HH = models.CharField(max_length=2, blank='True', null='True', default=None)
    MM = models.CharField(max_length=2, blank='True', null='True', default=None)
    SS = models.CharField(max_length=2, blank='True', null='True', default=None)
    
    location_description = models.CharField(max_length=100, blank='True', null='True', default=None)
    orientation = models.SmallIntegerField(blank='True', null='True', default=None)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)
    northing = models.FloatField(db_column='Northing', blank=True, null=True)
    citation = models.CharField(max_length=200, blank='True', null='True', default=None) #To hold a book or magazine reference
    citation_specifics = models.CharField(max_length=20, blank='True', null='True', default=None) #To hold the page or diagram number
    hyperlink = models.URLField(db_column='Hyperlink', blank=True, null=True, max_length=300)
    notes = models.TextField(blank='True', null='True', default=None)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return str(self.location_description) + " on " + str(self.DD) + "/" + str(self.MM) + "/" + str(self.YD) + str(self.YY)

class LocoSighting(models.Model): 
    sighting = models.ForeignKey(Sighting, on_delete=models.CASCADE)
    loco = models.ForeignKey(Locomotive, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.loco.number) + " at " + str(self.sighting.location_description)

class LocoClassSighting(models.Model):
    sighting = models.ForeignKey(Sighting, on_delete=models.CASCADE)
    loco_class = models.ForeignKey(LocoClass, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.loco_class.grouping_class) + " at " + str(self.sighting.location_description) 