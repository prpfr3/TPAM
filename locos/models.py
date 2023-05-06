from django.db import models
from notes.models import Post, Reference
import datetime


class WheelArrangement(models.Model):
    uic_system = models.CharField(
        db_column='UIC_system', max_length=20, blank=True, null=True)
    whyte_notation = models.CharField(
        db_column='Whyte_notation', max_length=20, blank=True, null=True)
    american_name = models.CharField(
        db_column='American_name', max_length=75, blank=True, null=True)
    visual = models.CharField(
        db_column='Visual', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.whyte_notation


class LocoClass(models.Model):

    SOURCE_TYPE = (
        (1, 'Wikipedia'),
        (2, 'Custom'),
    )

    wikiname = models.CharField(max_length=1000, blank=True, default='')
    brdslug = models.CharField(
        default=None, blank=True, null=True, max_length=255)

    br_power_class = models.CharField(max_length=5, blank=True, default='')
    wheel_body_type = models.CharField(max_length=100, blank=True, default='')
    wheel_arrangement = models.ForeignKey(WheelArrangement, default=None, blank=True,
                                          null=True, verbose_name="Wheel Arrangement", on_delete=models.SET_DEFAULT)
    year_built = models.CharField(max_length=100, blank=True, default='')
    number_range = models.CharField(max_length=100, blank=True, default='')
    number_range_slug = models.SlugField(
        default=None, blank=True, null=True, max_length=255)
    year_first_built = models.CharField(max_length=100, blank=True, default='')
    year_last_built = models.CharField(max_length=100, blank=True, default='')
    number_built = models.CharField(max_length=100, blank=True, default='')
    img_slug = models.SlugField(
        default=None, blank=True, null=True, max_length=255)
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
    boiler_tube_plates = models.CharField(
        max_length=200, blank=True, default='')
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
    heating_surface_firebox = models.CharField(
        max_length=200, blank=True, default='')
    heating_surface_tubes_flues = models.CharField(
        max_length=200, blank=True, default='')
    heating_surface_tubes = models.CharField(
        max_length=200, blank=True, default='')
    heating_surface_flues = models.CharField(
        max_length=200, blank=True, default='')
    height = models.CharField(max_length=200, blank=True, default='')
    height_pantograph = models.CharField(max_length=100, blank=True, default='')
    high_pressure_cylinder = models.CharField(
        max_length=200, blank=True, default='')
    leading_diameter = models.CharField(max_length=200, blank=True, default='')
    length_over_beams = models.CharField(max_length=200, blank=True, default='')
    length = models.CharField(max_length=200, blank=True, default='')
    loco_brake = models.CharField(max_length=200, blank=True, default='')
    loco_weight = models.CharField(max_length=250, blank=True, default='')
    low_pressure_cylinder = models.CharField(
        max_length=200, blank=True, default='')
    lubricant_capacity = models.CharField(
        max_length=100, blank=True, default='')
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
    power_output_one_hour = models.CharField(
        max_length=200, blank=True, default='')
    power_output_continuous = models.CharField(
        max_length=200, blank=True, default='')
    power_output_starting = models.CharField(
        max_length=200, blank=True, default='')
    power_type = models.CharField(max_length=200, blank=True, default='')
    prime_mover = models.CharField(max_length=200, blank=True, default='')
    rebuild_date = models.CharField(max_length=200, blank=True, default='')
    remanufacturer = models.CharField(max_length=200, blank=True, default='')
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
    wheel_configuration_aar = models.CharField(
        max_length=200, blank=True, default='')
    wheel_configuration_commonwealth = models.CharField(
        max_length=200, blank=True, default='')
    wheelbase = models.CharField(max_length=200, blank=True, default='')
    wheelbase_engine = models.CharField(max_length=200, blank=True, default='')
    wheelbase_tender = models.CharField(max_length=200, blank=True, default='')
    wheel_diameter = models.CharField(max_length=200, blank=True, default='')
    whyte = models.CharField(max_length=200, blank=True, default='')
    width = models.CharField(max_length=200, blank=True, default='')
    withdrawn = models.CharField(max_length=200, blank=True, default='')

    references = models.ManyToManyField(Reference, blank=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse
        return reverse('locos:loco_class', kwargs={'loco_class_id': self.pk})

    def __str__(self):
        return self.wikiname

    class Meta:
        verbose_name = 'Locomotive Class'
        verbose_name_plural = 'Locomotive Classes'
        managed = True


class LocoClassList(models.Model):
    name = models.CharField(max_length=1000, blank=True, default='')
    wikislug = models.SlugField(
        max_length=250, allow_unicode=True, default=None, blank=True, null=True)
    brdslug = models.CharField(default=None, null=True, max_length=255)
    lococlass_fk = models.ForeignKey(
        LocoClass, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Locomotive Class Mapping'
        verbose_name_plural = 'Locomotive Class Mappings'


class Locomotive(models.Model):
    identifier = models.CharField(max_length=500, blank=True, null=True)
    number_as_built = models.CharField(max_length=20, blank=True, null=True)
    number_pregrouping = models.CharField(max_length=20, blank=True, null=True)
    number_grouping = models.CharField(max_length=20, blank=True, null=True)
    number_postgrouping = models.CharField(max_length=20, blank=True, null=True)
    brd_slug = models.CharField(max_length=250, blank=True, null=True)
    order_number = models.CharField(max_length=30, blank=True, null=True)
    brd_order_number_slug = models.CharField(
        max_length=250, blank=True, null=True)
    works_number = models.CharField(max_length=30, blank=True, null=True)
    brd_class_name = models.CharField(max_length=250, blank=True, null=True)
    brd_class_name_slug = models.CharField(
        max_length=250, blank=True, null=True)
    order_number = models.CharField(max_length=20, blank=True, null=True)
    order_date = models.CharField(max_length=10, blank=True, null=True)
    order_datetime = models.DateField(blank=True, null=True)
    build_date = models.CharField(max_length=10, blank=True, null=True)
    build_datetime = models.DateField(blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    withdrawn_date = models.CharField(max_length=10, blank=True, null=True)
    withdrawn_datetime = models.DateField(blank=True, null=True)
    scrapped_date = models.CharField(max_length=10, blank=True, null=True)
    scrapped_datetime = models.DateField(blank=True, null=True)
    company_grouping_code = models.CharField(
        max_length=10, blank=True, null=True)
    company_pregrouping_code = models.CharField(
        max_length=10, blank=True, null=True)
    lococlass = models.ForeignKey(LocoClass, default=None, null=True, blank=True,
                                  verbose_name="Locomotive Class", on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=100, blank=True, null=True)

    references = models.ManyToManyField(Reference, blank=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.company_grouping_code} \
            {self.company_pregrouping_code} \
            {self.brd_class_name} Number as Built: \
            {self.number_as_built}"

    @property
    def age(self):
        today = datetime.date.today()
        age_years = (today.year - self.build_datetime.year) - int(
            (today.month, today.day) <
            (self.build_datetime.month, self.build_datetime.day))
        return age_years
