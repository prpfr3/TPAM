import sys
import datetime

from django.db import models
from notes.models import Post, Reference
from people.models import Person
from companies.models import Company, Manufacturer
from locations.models import HeritageSite, Visit
from django.conf import settings
from django.utils.html import format_html

sys.path.append("..")
from utils.utils import custom_slugify


class WheelArrangement(models.Model):
    uic_system = models.CharField(
        db_column="UIC_system", max_length=20, blank=True, null=True
    )
    whyte_notation = models.CharField(
        db_column="Whyte_notation", max_length=20, blank=True, null=True
    )
    american_name = models.CharField(
        db_column="American_name", max_length=75, blank=True, null=True
    )
    visual = models.CharField(db_column="Visual", max_length=20, blank=True, null=True)

    def __str__(self):
        return self.whyte_notation


class LocoClass(models.Model):
    slug = models.CharField(
        default=None, null=True, blank=True, max_length=255, unique=True, editable=False
    )
    name = models.CharField(max_length=1000, blank=True, default="")
    brdslug = models.CharField(default=None, blank=True, null=True, max_length=255)
    notes = models.TextField(default=None, blank=True, null=True)

    br_power_class = models.CharField(max_length=5, blank=True, default="")
    wheel_body_type = models.CharField(max_length=100, blank=True, default="")
    wheel_arrangement = models.ForeignKey(
        WheelArrangement,
        default=None,
        blank=True,
        null=True,
        verbose_name="Wheel Arrangement",
        on_delete=models.SET_DEFAULT,
    )
    year_built = models.CharField(max_length=100, blank=True, default="")
    number_range = models.CharField(max_length=100, blank=True, default="")
    number_range_slug = models.SlugField(
        default=None, blank=True, null=True, max_length=255
    )
    year_first_built = models.CharField(max_length=100, blank=True, default="")
    year_last_built = models.CharField(max_length=100, blank=True, default="")
    number_built = models.CharField(max_length=100, blank=True, default="")
    img_slug = models.SlugField(default=None, blank=True, null=True, max_length=255)
    adhesive_weight = models.CharField(max_length=200, blank=True, default="")
    adhesion_factor = models.CharField(max_length=40, blank=True, default="")
    alternator = models.CharField(max_length=75, blank=True, default="")
    axle_load = models.CharField(max_length=200, blank=True, default="")
    axle_load_class = models.CharField(max_length=200, blank=True, default="")
    bogie = models.CharField(max_length=100, blank=True, default="")
    bogies = models.CharField(max_length=100, blank=True, default="")
    boiler = models.CharField(max_length=200, blank=True, default="")
    boiler_pressure = models.CharField(max_length=200, blank=True, default="")
    boiler_diameter = models.CharField(max_length=200, blank=True, default="")
    boiler_model = models.CharField(max_length=200, blank=True, default="")
    boiler_pitch = models.CharField(max_length=200, blank=True, default="")
    boiler_tube_plates = models.CharField(max_length=200, blank=True, default="")
    brakeforce = models.CharField(max_length=200, blank=True, default="")
    build_date = models.CharField(max_length=200, blank=True, default="")
    coolant_capacity = models.CharField(max_length=50, blank=True, default="")
    couplers = models.CharField(max_length=50, blank=True, default="")
    coupled_diameter = models.CharField(max_length=50, blank=True, default="")
    current_pickups = models.CharField(max_length=300, blank=True, default="")
    cylinder_size = models.CharField(max_length=300, blank=True, default="")
    cylinders = models.CharField(max_length=125, blank=True, default="")
    displacement = models.CharField(max_length=200, blank=True, default="")
    disposition = models.CharField(max_length=200, blank=True, default="")
    driver_diameter = models.CharField(max_length=200, blank=True, default="")
    driving_unit_wheelbase = models.CharField(max_length=200, blank=True, default="")
    electric_systems = models.CharField(max_length=200, blank=True, default="")
    engine_maximum_rpm = models.CharField(max_length=50, blank=True, default="")
    engine_type = models.CharField(max_length=100, blank=True, default="")
    firegrate_area = models.CharField(max_length=100, blank=True, default="")
    fuel_capacity = models.CharField(max_length=200, blank=True, default="")
    fuel_type = models.CharField(max_length=100, blank=True, default="")
    gauge = models.CharField(max_length=175, blank=True, default="")
    gear_ratio = models.CharField(max_length=100, blank=True, default="")
    generator = models.CharField(max_length=150, blank=True, default="")
    heating_area = models.CharField(max_length=200, blank=True, default="")
    heating_surface = models.CharField(max_length=200, blank=True, default="")
    heating_surface_firebox = models.CharField(max_length=200, blank=True, default="")
    heating_surface_tubes_flues = models.CharField(
        max_length=200, blank=True, default=""
    )
    heating_surface_tubes = models.CharField(max_length=200, blank=True, default="")
    heating_surface_flues = models.CharField(max_length=200, blank=True, default="")
    height = models.CharField(max_length=200, blank=True, default="")
    height_pantograph = models.CharField(max_length=100, blank=True, default="")
    high_pressure_cylinder = models.CharField(max_length=200, blank=True, default="")
    leading_diameter = models.CharField(max_length=200, blank=True, default="")
    length_over_beams = models.CharField(max_length=200, blank=True, default="")
    length_over_buffers = models.CharField(max_length=200, blank=True, default="")
    length = models.CharField(max_length=200, blank=True, default="")
    loco_brake = models.CharField(max_length=200, blank=True, default="")
    loco_weight = models.CharField(max_length=250, blank=True, default="")
    low_pressure_cylinder = models.CharField(max_length=200, blank=True, default="")
    lubricant_capacity = models.CharField(max_length=100, blank=True, default="")
    model = models.CharField(max_length=100, blank=True, default="")
    maximum_speed = models.CharField(max_length=200, blank=True, default="")
    minimum_curve = models.CharField(max_length=200, blank=True, default="")
    mu_working = models.CharField(max_length=200, blank=True, default="")
    nicknames = models.CharField(max_length=200, blank=True, default="")
    number_in_class = models.CharField(max_length=200, blank=True, default="")
    number_rebuilt = models.CharField(max_length=200, blank=True, default="")
    numbers = models.CharField(max_length=700, blank=True, default="")
    number_of_tubes = models.CharField(max_length=700, blank=True, default="")
    official_name = models.CharField(max_length=200, blank=True, default="")
    order_number = models.CharField(max_length=200, blank=True, default="")
    pivot_centres = models.CharField(max_length=200, blank=True, default="")
    pony_wheel_diameter = models.CharField(max_length=200, blank=True, default="")
    power_class = models.CharField(max_length=200, blank=True, default="")
    power_output = models.CharField(max_length=200, blank=True, default="")
    power_output_one_hour = models.CharField(max_length=200, blank=True, default="")
    power_output_continuous = models.CharField(max_length=200, blank=True, default="")
    power_output_starting = models.CharField(max_length=200, blank=True, default="")
    power_type = models.CharField(max_length=200, blank=True, default="")
    prime_mover = models.CharField(max_length=200, blank=True, default="")
    rebuild_date = models.CharField(max_length=200, blank=True, default="")
    remanufacturer = models.CharField(max_length=200, blank=True, default="")
    retired = models.CharField(max_length=200, blank=True, default="")
    rpm_range = models.CharField(max_length=200, blank=True, default="")
    safety_systems = models.CharField(max_length=200, blank=True, default="")
    serial_number = models.CharField(max_length=250, blank=True, default="")
    superheater_type = models.CharField(max_length=200, blank=True, default="")
    superheater_elements = models.CharField(max_length=200, blank=True, default="")
    tender_capacity = models.CharField(max_length=200, blank=True, default="")
    tender_type = models.CharField(max_length=200, blank=True, default="")
    tender_weight = models.CharField(max_length=300, blank=True, default="")
    total_weight = models.CharField(max_length=200, blank=True, default="")
    tractive_effort = models.CharField(max_length=1000, blank=True, default="")
    traction_motors = models.CharField(max_length=200, blank=True, default="")
    trailing_diameter = models.CharField(max_length=200, blank=True, default="")
    train_brakes = models.CharField(max_length=200, blank=True, default="")
    train_heating = models.CharField(max_length=200, blank=True, default="")
    transmission = models.CharField(max_length=200, blank=True, default="")
    tube_length = models.CharField(max_length=200, blank=True, default="")
    tube_diameter_outside = models.CharField(max_length=200, blank=True, default="")
    UIC = models.CharField(max_length=200, blank=True, default="")
    valve_gear = models.CharField(max_length=200, blank=True, default="")
    valve_type = models.CharField(max_length=200, blank=True, default="")
    water_capacity = models.CharField(max_length=300, blank=True, default="")
    wheel_configuration_aar = models.CharField(max_length=200, blank=True, default="")
    wheel_configuration_commonwealth = models.CharField(
        max_length=200, blank=True, default=""
    )
    wheelbase = models.CharField(max_length=200, blank=True, default="")
    wheelbase_engine = models.CharField(max_length=200, blank=True, default="")
    wheelbase_tender = models.CharField(max_length=200, blank=True, default="")
    wheel_diameter = models.CharField(max_length=200, blank=True, default="")
    whyte = models.CharField(max_length=200, blank=True, default="")
    width = models.CharField(max_length=200, blank=True, default="")
    withdrawn = models.CharField(max_length=200, blank=True, default="")
    posts = models.ManyToManyField(Post, related_name="lococlass_posts", blank=True)

    designer_person = models.ForeignKey(
        Person, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    designer_company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )

    references = models.ManyToManyField(
        Reference, related_name="lococlass_references", blank=True
    )

    owner_operators = models.ManyToManyField(
        Company, related_name="lococlass_owner_operators", blank=True
    )
    manufacturers = models.ManyToManyField(
        Manufacturer, related_name="lococlass_manufacturers", blank=True
    )

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse

        return reverse("locos:loco_class", kwargs={"loco_class_id": self.pk})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.classes = self.name.split(";")
        self.slug = self.classes[0].replace(" ", "_").replace("/", "%2F")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Locomotive Class"
        verbose_name_plural = "Locomotive Classes"
        managed = True


class Locomotive(models.Model):
    number_as_built = models.CharField(max_length=20, blank=True, null=True)
    number_pregrouping_1 = models.CharField(max_length=20, blank=True, null=True)
    number_pregrouping_1_date = models.CharField(max_length=10, blank=True, null=True)
    number_pregrouping_2 = models.CharField(max_length=20, blank=True, null=True)
    number_pregrouping_2_date = models.CharField(max_length=10, blank=True, null=True)
    number_grouping_1 = models.CharField(max_length=20, blank=True, null=True)
    number_grouping_1_date = models.CharField(max_length=10, blank=True, null=True)
    number_grouping_2 = models.CharField(max_length=20, blank=True, null=True)
    number_grouping_2_date = models.CharField(max_length=10, blank=True, null=True)
    number_postgrouping_1 = models.CharField(max_length=20, blank=True, null=True)
    number_postgrouping_1_date = models.CharField(max_length=10, blank=True, null=True)
    number_postgrouping_2 = models.CharField(max_length=20, blank=True, null=True)
    number_postgrouping_2_date = models.CharField(max_length=10, blank=True, null=True)
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
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    withdrawn_date = models.CharField(max_length=10, blank=True, null=True)
    withdrawn_datetime = models.DateField(blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True)
    scrapped_date = models.CharField(max_length=10, blank=True, null=True)
    scrapped_datetime = models.DateField(blank=True, null=True)
    company_grouping_code = models.CharField(max_length=10, blank=True, null=True)
    company_pregrouping_code = models.CharField(max_length=10, blank=True, null=True)
    lococlass = models.ForeignKey(
        LocoClass,
        default=None,
        null=True,
        blank=True,
        verbose_name="Locomotive Class",
        on_delete=models.SET_DEFAULT,
    )
    name = models.CharField(max_length=100, blank=True, null=True)

    references = models.ManyToManyField(Reference, blank=True)
    notes = models.TextField(blank=True, null=True)
    posts = models.ManyToManyField(Post, related_name="loco_posts", blank=True)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("locos:locomotive", kwargs={"locomotive_id": self.pk})

    def __str__(self):
        parts = []

        if self.lococlass is not None:
            parts.append(f"{self.lococlass}")

        if self.number_as_built is not None:
            parts.append(f"Number as Built: {self.number_as_built}")

        return " ".join(parts)

    @property
    def age(self):
        today = datetime.date.today()
        return (today.year - self.build_datetime.year) - int(
            (today.month, today.day)
            < (self.build_datetime.month, self.build_datetime.day)
        )


class Image(models.Model):
    image_name = models.CharField(max_length=100, default=None)
    image = models.ImageField(upload_to="images/")
    lococlass = models.ManyToManyField(
        LocoClass, related_name="lococlass_images", blank=True
    )
    location = models.ForeignKey(
        HeritageSite,
        default=None,
        blank=True,
        null=True,
        verbose_name="Location",
        on_delete=models.SET_DEFAULT,
    )
    visit = models.ForeignKey(
        Visit,
        default=None,
        blank=True,
        null=True,
        verbose_name="Visit",
        on_delete=models.SET_DEFAULT,
    )
    notes = models.TextField(default=None, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Railway Image"
        verbose_name_plural = "Railway Images"

    def __str__(self):
        return self.image_name


class Fav(models.Model):
    thing = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="railway_image_favs_users",
    )

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ("thing", "user")
        verbose_name = "Railway Image Favourite"
        verbose_name_plural = "Railway Image Favourites"

    def __str__(self):
        return f"{self.user} likes {self.thing.image_name[:10]}"


class BMImage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # Needed because of similar relationships in other appas
        related_name="images_liked",
        blank=True,
    )

    class Meta:
        verbose_name = "Railway Bookmarked Image"
        verbose_name_plural = "Railway Bookmarked Images"

    def __str__(self):
        return self.title
