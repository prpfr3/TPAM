from django.contrib.gis.db import models
from locations.models import Route, Location, ELR, RouteMap

class WheelArrangement(models.Model):
    uic_system = models.CharField(db_column='UIC_system', max_length=20, blank=True, null=True)
    whyte_notation = models.CharField(db_column='Whyte_notation', max_length=20, blank=True, null=True)
    american_name = models.CharField(db_column='American_name', max_length=75, blank=True, null=True)
    visual = models.CharField(db_column='Visual', max_length=20, blank=True, null=True)
    def __str__(self):
      return self.whyte_notation

class LocoClass(models.Model):
  wikiname = models.CharField(max_length=1000, blank=True, default='')
  brdslug = models.CharField(default=None, blank=True, null=True, max_length=255)

  br_power_class = models.CharField(max_length=5, blank=True, default='')
  wheel_body_type = models.CharField(max_length=100, blank=True, default='')
  wheel_arrangement = models.ForeignKey(WheelArrangement, default=None, blank=True, null=True, verbose_name="Wheel Arrangement", on_delete=models.SET_DEFAULT)
  year_built = models.CharField(max_length=100, blank=True, default='')
  number_range = models.CharField(max_length=100, blank=True, default='')
  number_range_slug = models.SlugField(default=None, blank=True, null=True, max_length=255)
  year_first_built = models.CharField(max_length=100, blank=True, default='')
  year_last_built = models.CharField(max_length=100, blank=True, default='')
  number_built = models.CharField(max_length=100, blank=True, default='')
  img_slug = models.SlugField(default=None, blank=True, null=True, max_length=255)
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
  tractive_effort = models.CharField(max_length=1000, blank=True, default='')
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
    return self.wikiname

class LocoClassList(models.Model):
  name = models.CharField(max_length=1000, blank=True, default='')
  wikislug = models.CharField(default=None, null=True, max_length=255)
  brdslug = models.CharField(default=None, null=True, max_length=255)
  lococlass_fk = models.ForeignKey(LocoClass, blank=True, null=True, on_delete=models.CASCADE)
  def __str__(self):
    return self.name

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
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="person_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="person_builder")
  def __str__(self):
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
      return f"{self.person.name} {self.role.role}"

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
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="builder_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="builder_builder")
  def __str__(self):
    return self.name
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
  company_categories = models.ManyToManyField(CompanyCategory)
  lococlass_owneroperator = models.ManyToManyField(LocoClass, through='ClassOwnerOperator', related_name="company_owneroperator")
  lococlass_designed = models.ManyToManyField(LocoClass, through='ClassDesigner', related_name="company_designer")
  lococlass_built = models.ManyToManyField(LocoClass, through='ClassBuilder', related_name="company_builder")
  route_owneroperator = models.ManyToManyField(Route, through='RouteOwnerOperator', related_name="route_owneroperator")
  def __str__(self):
    return self.name or ""
  class Meta:
    verbose_name_plural = 'Companies'

class RouteOwnerOperator(models.Model): 
  route_fk = models.ForeignKey(Route, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, on_delete=models.CASCADE)
  def __str__(self):
      return f"{self.route_fk} {self.company_fk}"

class ClassBuilder(models.Model): 
  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  builder_fk = models.ForeignKey(Builder, blank=True, null=True, on_delete=models.CASCADE)
  person_fk = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
  def __str__(self):
      if self.person_fk is not None:
        builder = self.person_fk.name
      elif self.builder_fk is not None:
        builder = self.builder_fk.name
      elif self.company_fk is not None:
        builder = self.company_fk.name
      else:
        builder = ""
      return f"{builder}"

class ClassDesigner(models.Model): 
  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  builder_fk = models.ForeignKey(Builder, blank=True, null=True, on_delete=models.CASCADE)
  person_fk = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
  def __str__(self):
      if self.person_fk is not None:
        designer = self.person_fk.name
      elif self.builder_fk is not None:
        designer = self.builder_fk.name
      elif self.company_fk is not None:
        designer = self.company_fk.name
      else:
        designer = ""
      return f"{designer}"

class ClassOwnerOperator(models.Model): 
  lococlass_fk = models.ForeignKey(LocoClass, on_delete=models.CASCADE)
  company_fk = models.ForeignKey(Company, on_delete=models.CASCADE)
  def __str__(self):
      return f"{self.lococlass_fk} {self.company_fk}"

class Locomotive(models.Model):
  identifier = models.CharField(max_length=500, blank=True, null=True)
  number_as_built = models.CharField(max_length=20, blank=True, null=True)
  number_pregrouping = models.CharField(max_length=20, blank=True, null=True)
  number_grouping = models.CharField(max_length=20, blank=True, null=True)
  number_postgrouping = models.CharField(max_length=20, blank=True, null=True)
  brd_slug = models.CharField(max_length=250, blank=True, null=True)
  order_number = models.CharField(max_length=30, blank=True, null=True)
  brd_order_number_slug = models.CharField(max_length=250, blank=True, null=True)
  works_number = models.CharField(max_length=30, blank=True, null=True)
  brd_class_name = models.CharField(max_length=250, blank=True, null=True)
  brd_class_name_slug = models.CharField(max_length=250, blank=True, null=True)
  order_number = models.CharField(max_length=20, blank=True, null=True)
  order_date = models.CharField(max_length=10, blank=True, null=True)
  order_datetime = models.DateField(blank=True, null=True)
  build_date = models.CharField(max_length=10, blank=True, null=True)
  build_datetime = models.DateField(blank=True, null=True)
  builder = models.CharField(max_length=50, blank=True, null=True)
  withdrawn_date = models.CharField(max_length=10, blank=True, null=True)
  withdrawn_datetime = models.DateField(blank=True, null=True)
  scrapped_date = models.CharField(max_length=10, blank=True, null=True)
  scrapped_datetime = models.DateField(blank=True, null=True)
  company_grouping_code = models.CharField(max_length=10, blank=True, null=True)
  company_pregrouping_code = models.CharField(max_length=10, blank=True, null=True)
  lococlass = models.ForeignKey(LocoClass, default=None, null=True, blank=True, verbose_name="Locomotive Class", on_delete=models.SET_DEFAULT)
  name = models.CharField(max_length=100, blank=True, null=True)
  notes = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.company_grouping_code} \
            {self.company_pregrouping_code} \
            {self.brd_class_name}: Number as Built \
            {self.number_pregrouping}"

class Reference(models.Model):
    REFERENCE_TYPE = (
      ( 1, 'Book'),
      ( 2, 'Website'),
      ( 3, 'Magazine'),
      ( 4, 'Video'),
      ( 5, 'MySighting'),
      ( 6, 'MyPhoto'),
    )
    ref = models.IntegerField()
    type = models.IntegerField(choices=REFERENCE_TYPE, default=1,)
    citation = models.TextField(blank='True', null='True', 
        default='cite book | last1 = | first1 = | title = [[ ]] | publisher = [[]] | pages = 1-2  | date = ??/??/?? | isbn = 0-786918-50-0 | journal = | volume = | issue = | issn = ')
    url = models.URLField(blank=True, null=True, max_length=300)
    notes = models.TextField(blank='True', null='True', default=None)
    locos = models.ManyToManyField(Locomotive, through='LocoClassSighting', blank='True')
    lococlass = models.ManyToManyField(LocoClass, through='LocoClassSighting', blank='True')
    date = models.CharField(max_length=20, blank='True', null='True', default='??/??/?? ??:??:??')
    route_fk  = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True, default=None)
    routemap_fk  = models.ForeignKey(RouteMap, on_delete=models.CASCADE, blank=True, null=True, default=None)
    location_fk  = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, default=None)
    location_description = models.CharField(max_length=100, blank='True', null='True', default=None)
    company_fk = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, default=None)
    ELR_fk = models.ForeignKey(ELR, on_delete=models.CASCADE, blank=True, null=True, default=None)
    visit = models.ForeignKey('maps.Visit', blank=True, null=True, default=None, verbose_name="Visit", on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{str(self.get_type_display())}: {str(self.citation)}"

class LocoClassSighting(models.Model):
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    loco_class = models.ForeignKey(LocoClass, blank=True, null=True, on_delete=models.CASCADE)
    loco = models.ForeignKey(Locomotive, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{str(self.loco_class.wikiname)} at {str(self.reference.location_description)}"