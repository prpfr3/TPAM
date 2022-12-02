BASE_DIR =  D:\OneDrive\Source\Python Projects\TPAM
cwd='D:\\OneDrive\\Source\\Python Projects\\TPAM'
Using development/local settings from settings.py.
Static directory is D:\OneDrive\Source\Python Projects\TPAM\static given a base directory of D:\OneDrive\Source\Python Projects\TPAM
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AircraftAirbmimage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'aircraft_airbmimage'


class AircraftAirbmimageUsersLike(models.Model):
    airbmimage = models.ForeignKey(AircraftAirbmimage, models.DO_NOTHING)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'aircraft_airbmimage_users_like'
        unique_together = (('airbmimage', 'user'),)


class AircraftAircraftclass(models.Model):
    airclass = models.CharField(max_length=100, blank=True, null=True)
    wikislug = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'aircraft_aircraftclass'


class AircraftAirimage(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    notes = models.TextField()
    date_added = models.DateTimeField()
    airclass = models.ForeignKey(AircraftAircraftclass, models.DO_NOTHING)
    location = models.ForeignKey('MapsHeritagesite', models.DO_NOTHING)
    visit = models.ForeignKey('MapsVisit', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'aircraft_airimage'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class LocosBuilder(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.CharField(max_length=200)
    railuk_builder_code = models.CharField(max_length=3, blank=True, null=True)
    brd_builder_code = models.CharField(max_length=3, blank=True, null=True)
    brsl_builder_code = models.CharField(max_length=10, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    pre_grouping_owner = models.CharField(max_length=10)
    grouping_owner = models.CharField(max_length=4)
    br_region_owner = models.CharField(max_length=3)
    date_opened = models.CharField(max_length=10, blank=True, null=True)
    date_closed = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=77, blank=True, null=True)
    steam = models.CharField(max_length=10, blank=True, null=True)
    diesel = models.CharField(max_length=10, blank=True, null=True)
    electric = models.CharField(max_length=10, blank=True, null=True)
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_builder'


class LocosClassbuilder(models.Model):
    builder_fk = models.ForeignKey(LocosBuilder, models.DO_NOTHING, blank=True, null=True)
    company_fk = models.ForeignKey('LocosCompany', models.DO_NOTHING, blank=True, null=True)
    lococlass_fk = models.ForeignKey('LocosLococlass', models.DO_NOTHING)
    person_fk = models.ForeignKey('LocosPerson', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_classbuilder'


class LocosClassdesigner(models.Model):
    builder_fk = models.ForeignKey(LocosBuilder, models.DO_NOTHING, blank=True, null=True)
    company_fk = models.ForeignKey('LocosCompany', models.DO_NOTHING, blank=True, null=True)
    lococlass_fk = models.ForeignKey('LocosLococlass', models.DO_NOTHING)
    person_fk = models.ForeignKey('LocosPerson', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_classdesigner'


class LocosClassowneroperator(models.Model):
    company_fk = models.ForeignKey('LocosCompany', models.DO_NOTHING)
    lococlass_fk = models.ForeignKey('LocosLococlass', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_classowneroperator'


class LocosClosedRouteGeodata(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    geometry = models.GeometryField(dim=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_closed_routes_geodata'


class LocosCompany(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.CharField(max_length=200)
    code = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_company'


class LocosCompanyCompanyCategories(models.Model):
    company = models.ForeignKey(LocosCompany, models.DO_NOTHING)
    companycategory = models.ForeignKey('LocosCompanycategory', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_company_company_categories'
        unique_together = (('company', 'companycategory'),)


class LocosCompanycategory(models.Model):
    category = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_companycategory'


class LocosDepot(models.Model):
    depot = models.CharField(max_length=1000, blank=True, null=True)
    codes = models.CharField(max_length=100, blank=True, null=True)
    code_dates = models.CharField(max_length=100, blank=True, null=True)
    date_opened = models.CharField(max_length=20, blank=True, null=True)
    date_closed_to_steam = models.CharField(max_length=20, blank=True, null=True)
    date_closed = models.CharField(max_length=20, blank=True, null=True)
    br_region = models.CharField(db_column='BR_region', max_length=20, blank=True, null=True)  # Field name made lowercase.
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    comments = models.TextField()
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'locos_depots'


class LocosImage(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    notes = models.TextField()
    date_added = models.DateTimeField()
    location = models.ForeignKey('MapsHeritagesite', models.DO_NOTHING)
    visit = models.ForeignKey('MapsVisit', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_image'


class LocosLococlass(models.Model):
    wikipedia_name = models.CharField(max_length=1000)
    br_power_class = models.CharField(max_length=5)
    wheel_body_type = models.CharField(max_length=100)
    year_built = models.CharField(max_length=100)
    number_range = models.CharField(max_length=100)
    number_range_slug = models.CharField(max_length=255, blank=True, null=True)
    year_first_built = models.CharField(max_length=100)
    year_last_built = models.CharField(max_length=100)
    number_built = models.CharField(max_length=100)
    img_slug = models.CharField(max_length=255, blank=True, null=True)
    wheel_arrangement = models.ForeignKey('LocosWheelarrangement', models.DO_NOTHING, blank=True, null=True)
    adhesive_weight = models.CharField(max_length=200)
    axle_load = models.CharField(max_length=200)
    boiler = models.CharField(max_length=200)
    boiler_diameter = models.CharField(max_length=200)
    boiler_model = models.CharField(max_length=200)
    boiler_pitch = models.CharField(max_length=200)
    boiler_pressure = models.CharField(max_length=200)
    boiler_tube_plates = models.CharField(max_length=200)
    adhesion_factor = models.CharField(max_length=40)
    build_date = models.CharField(max_length=200)
    coupled_diameter = models.CharField(max_length=50)
    cylinder_size = models.CharField(max_length=300)
    cylinders = models.CharField(max_length=125)
    disposition = models.CharField(max_length=200)
    driver_diameter = models.CharField(max_length=200)
    firegrate_area = models.CharField(max_length=100)
    fuel_capacity = models.CharField(max_length=200)
    fuel_type = models.CharField(max_length=100)
    uic = models.CharField(db_column='UIC', max_length=200)  # Field name made lowercase.
    gauge = models.CharField(max_length=175)
    heating_area = models.CharField(max_length=200)
    heating_surface = models.CharField(max_length=200)
    heating_surface_firebox = models.CharField(max_length=200)
    heating_surface_flues = models.CharField(max_length=200)
    heating_surface_tubes = models.CharField(max_length=200)
    heating_surface_tubes_flues = models.CharField(max_length=200)
    height = models.CharField(max_length=200)
    high_pressure_cylinder = models.CharField(max_length=200)
    leading_diameter = models.CharField(max_length=200)
    length = models.CharField(max_length=200)
    length_over_beams = models.CharField(max_length=200)
    loco_brake = models.CharField(max_length=200)
    loco_weight = models.CharField(max_length=250)
    low_pressure_cylinder = models.CharField(max_length=200)
    maximum_speed = models.CharField(max_length=200)
    minimum_curve = models.CharField(max_length=200)
    nicknames = models.CharField(max_length=200)
    number_in_class = models.CharField(max_length=200)
    numbers = models.CharField(max_length=700)
    number_rebuilt = models.CharField(max_length=200)
    official_name = models.CharField(max_length=200)
    order_number = models.CharField(max_length=200)
    power_class = models.CharField(max_length=200)
    power_type = models.CharField(max_length=200)
    rebuild_date = models.CharField(max_length=200)
    rebuilder = models.CharField(max_length=200)
    retired = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=250)
    superheater_type = models.CharField(max_length=200)
    tender_capacity = models.CharField(max_length=200)
    tender_type = models.CharField(max_length=200)
    tender_weight = models.CharField(max_length=300)
    total_weight = models.CharField(max_length=200)
    tractive_effort = models.CharField(max_length=1000)
    trailing_diameter = models.CharField(max_length=200)
    train_brakes = models.CharField(max_length=200)
    train_heating = models.CharField(max_length=200)
    valve_gear = models.CharField(max_length=200)
    valve_type = models.CharField(max_length=200)
    water_capacity = models.CharField(max_length=300)
    wheelbase = models.CharField(max_length=200)
    wheelbase_engine = models.CharField(max_length=200)
    wheelbase_tender = models.CharField(max_length=200)
    whyte = models.CharField(max_length=200)
    width = models.CharField(max_length=200)
    withdrawn = models.CharField(max_length=200)
    alternator = models.CharField(max_length=75)
    axle_load_class = models.CharField(max_length=200)
    bogie = models.CharField(max_length=100)
    bogies = models.CharField(max_length=100)
    brakeforce = models.CharField(max_length=200)
    coolant_capacity = models.CharField(max_length=50)
    couplers = models.CharField(max_length=50)
    current_pickups = models.CharField(max_length=300)
    displacement = models.CharField(max_length=200)
    electric_systems = models.CharField(max_length=200)
    engine_maximum_rpm = models.CharField(max_length=50)
    engine_type = models.CharField(max_length=100)
    gear_ratio = models.CharField(max_length=100)
    generator = models.CharField(max_length=150)
    height_pantograph = models.CharField(max_length=100)
    lubricant_capacity = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    mu_working = models.CharField(max_length=200)
    pivot_centres = models.CharField(max_length=200)
    power_output = models.CharField(max_length=200)
    power_output_continuous = models.CharField(max_length=200)
    power_output_one_hour = models.CharField(max_length=200)
    power_output_starting = models.CharField(max_length=200)
    prime_mover = models.CharField(max_length=200)
    rpm_range = models.CharField(max_length=200)
    safety_systems = models.CharField(max_length=200)
    traction_motors = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    wheel_configuration_aar = models.CharField(max_length=200)
    wheel_configuration_commonwealth = models.CharField(max_length=200)
    wheel_diameter = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'locos_lococlass'


class LocosLococlassimage(models.Model):
    image = models.ForeignKey(LocosImage, models.DO_NOTHING)
    loco_class = models.ForeignKey(LocosLococlass, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_lococlassimage'


class LocosLococlasslist(models.Model):
    name = models.CharField(max_length=1000)
    wikislug = models.CharField(max_length=255, blank=True, null=True)
    lococlass_fk = models.ForeignKey(LocosLococlass, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_lococlasslist'


class LocosLococlasssighting(models.Model):
    loco_class = models.ForeignKey(LocosLococlass, models.DO_NOTHING)
    reference = models.ForeignKey('LocosSighting', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_lococlasssighting'


class LocosLocoimage(models.Model):
    loco_status = models.IntegerField()
    image = models.ForeignKey(LocosImage, models.DO_NOTHING)
    loco = models.ForeignKey('LocosLocomotive', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_locoimage'


class LocosLocomotive(models.Model):
    build_date = models.CharField(max_length=10, blank=True, null=True)
    wikipedia_name = models.CharField(max_length=10, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    wheel_arrangement = models.CharField(max_length=10, blank=True, null=True)
    designer = models.CharField(max_length=30, blank=True, null=True)
    builder = models.CharField(max_length=50, blank=True, null=True)
    order_number = models.CharField(max_length=30, blank=True, null=True)
    works_number = models.CharField(max_length=30, blank=True, null=True)
    withdrawn = models.CharField(max_length=15, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    lococlass = models.ForeignKey(LocosLococlass, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_locomotive'


class LocosLocosighting(models.Model):
    loco = models.ForeignKey(LocosLocomotive, models.DO_NOTHING)
    reference = models.ForeignKey('LocosSighting', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_locosighting'


class LocosPerson(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    date_added = models.DateTimeField()
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    diedplace = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    gracetextslug = models.CharField(max_length=200)
    wikiimageslug = models.CharField(max_length=200)
    wikiimagetext = models.CharField(max_length=200)
    wikitextslug = models.CharField(max_length=200)
    birthplace = models.CharField(max_length=200)
    birthdate = models.CharField(max_length=10)
    dieddate = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'locos_person'


class LocosPersonrole(models.Model):
    person = models.ForeignKey(LocosPerson, models.DO_NOTHING)
    role = models.ForeignKey('LocosRole', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'locos_personrole'


class LocosRole(models.Model):
    role = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_role'

class LocosSighting(models.Model):
    dd = models.CharField(db_column='DD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    yd = models.CharField(db_column='YD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    yy = models.CharField(db_column='YY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hh = models.CharField(db_column='HH', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mm = models.CharField(db_column='MM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ss = models.CharField(db_column='SS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    location_description = models.CharField(max_length=100, blank=True, null=True)
    easting = models.FloatField(db_column='Easting', blank=True, null=True)  # Field name made lowercase.
    northing = models.FloatField(db_column='Northing', blank=True, null=True)  # Field name made lowercase.
    citation = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()
    type = models.IntegerField()
    short_description = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locos_sighting'


class LocosWheelarrangement(models.Model):
    uic_system = models.CharField(db_column='UIC_system', max_length=20, blank=True, null=True)  # Field name made lowercase.
    whyte_notation = models.CharField(db_column='Whyte_notation', max_length=20, blank=True, null=True)  # Field name made lowercase.
    american_name = models.CharField(db_column='American_name', max_length=75, blank=True, null=True)  # Field name made lowercase.
    visual = models.CharField(db_column='Visual', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'locos_wheelarrangement'


class MainmenuMydjangoapp(models.Model):
    image = models.CharField(max_length=100)
    summary = models.TextField()
    url = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mainmenu_mydjangoapp'


class MainmenuProfile(models.Model):
    bio = models.TextField()
    avatar = models.CharField(max_length=100)
    updated = models.DateTimeField()
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mainmenu_profile'


class MapsCitation(models.Model):
    author = models.CharField(max_length=10, blank=True, null=True)
    author_last = models.CharField(max_length=10, blank=True, null=True)
    author_first = models.CharField(max_length=10, blank=True, null=True)
    author_link = models.CharField(max_length=10, blank=True, null=True)
    editor = models.CharField(max_length=10, blank=True, null=True)
    editor_last = models.CharField(max_length=10, blank=True, null=True)
    editor_first = models.CharField(max_length=10, blank=True, null=True)
    editor_link = models.CharField(max_length=10, blank=True, null=True)
    publication_date = models.CharField(max_length=20, blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    chapter = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    edition = models.CharField(max_length=10, blank=True, null=True)
    series = models.CharField(max_length=10, blank=True, null=True)
    volume = models.CharField(max_length=10, blank=True, null=True)
    issue = models.CharField(max_length=10, blank=True, null=True)
    publisher = models.CharField(max_length=10, blank=True, null=True)
    page = models.CharField(max_length=10, blank=True, null=True)
    pages = models.CharField(max_length=10, blank=True, null=True)
    no_pp = models.CharField(max_length=10, blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    issn = models.CharField(max_length=20, blank=True, null=True)
    doi = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    access_date = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maps_citation'


class MapsHeritagesite(models.Model):
    name = models.CharField(max_length=100)
    wikislug = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()
    type = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    tpam_type = models.ForeignKey(MainmenuMydjangoapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'maps_heritagesite'


class MapsPost(models.Model):
    title = models.CharField(max_length=250)
    url = models.CharField(max_length=200, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    publish = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    status = models.CharField(max_length=10)
    owner = models.ForeignKey(MainmenuProfile, models.DO_NOTHING)
    topic = models.ForeignKey('MapsTopic', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'maps_post'


class MapsPostLiked(models.Model):
    post = models.ForeignKey(MapsPost, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'maps_post_liked'
        unique_together = (('post', 'user'),)


class MapsTopic(models.Model):
    text = models.CharField(max_length=25)
    date_added = models.DateTimeField()
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING)
    type = models.ForeignKey(MainmenuMydjangoapp, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'maps_topic'


class MapsVisit(models.Model):
    date = models.DateField()
    notes = models.TextField()
    date_added = models.DateField()
    location = models.ForeignKey(MapsHeritagesite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'maps_visit'


class MvsFav(models.Model):
    thing = models.ForeignKey('MvsMilitaryvehicleclass', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mvs_fav'
        unique_together = (('thing', 'user'),)


class MvsHeritagesite(models.Model):
    site_name = models.CharField(max_length=100)
    wikislug = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mvs_heritagesite'


class MvsMilitaryvehicleclass(models.Model):
    mvclass = models.CharField(max_length=100, blank=True, null=True)
    wikislug = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'mvs_militaryvehicleclass'


class MvsMvbmimage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mvs_mvbmimage'


class MvsMvbmimageUsersLike(models.Model):
    mvbmimage = models.ForeignKey(MvsMvbmimage, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mvs_mvbmimage_users_like'
        unique_together = (('mvbmimage', 'user'),)


class MvsMvimage(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    notes = models.TextField()
    date_added = models.DateTimeField()
    location = models.ForeignKey(MvsHeritagesite, models.DO_NOTHING)
    mvclass = models.ForeignKey(MvsMilitaryvehicleclass, models.DO_NOTHING)
    visit = models.ForeignKey('MvsVisit', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mvs_mvimage'


class MvsVisit(models.Model):
    date = models.DateField()
    notes = models.TextField()
    date_added = models.DateField()
    location = models.ForeignKey(MvsHeritagesite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mvs_visit'


class OsmhistoryRailRoutes(models.Model):
    id = models.TextField(blank=True, null=True)
    field_id = models.TextField(db_column='@id', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    building = models.TextField(blank=True, null=True)
    layer = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    public_transport = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    start_date = models.TextField(blank=True, null=True)
    train = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    wikidata = models.TextField(blank=True, null=True)
    wikipedia = models.TextField(blank=True, null=True)
    start_date_note = models.TextField(db_column='start_date:note', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    area = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    building_levels = models.TextField(db_column='building:levels', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    structure = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    name_1863_1908 = models.TextField(db_column='name:1863-1908', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    alt_name = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    name_1848_1966 = models.TextField(db_column='name:1848-1966', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1966_2021 = models.TextField(db_column='name:1966-2021', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    architect = models.TextField(blank=True, null=True)
    architect_wikipedia = models.TextField(db_column='architect:wikipedia', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1847_1922 = models.TextField(db_column='name:1847-1922', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1922 = models.TextField(db_column='name:1922', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    company_1898 = models.TextField(db_column='company:1898', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    company_end = models.TextField(db_column='company:end', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    company_start = models.TextField(db_column='company:start', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    end_date_goods = models.TextField(db_column='end_date:goods', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    gauge = models.TextField(blank=True, null=True)
    start_date_gwr = models.TextField(db_column='start_date:GWR', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    embankment = models.TextField(blank=True, null=True)
    bridge = models.TextField(blank=True, null=True)
    tracks = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    name_1 = models.TextField(blank=True, null=True)
    cutting = models.TextField(blank=True, null=True)
    man_made = models.TextField(blank=True, null=True)
    tunnel = models.TextField(blank=True, null=True)
    tram = models.TextField(blank=True, null=True)
    highway = models.TextField(blank=True, null=True)
    surface = models.TextField(blank=True, null=True)
    ford = models.TextField(blank=True, null=True)
    level = models.TextField(blank=True, null=True)
    fixme = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    electrified = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    end_date_edtf = models.TextField(db_column='end_date:edtf', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    end_date_note = models.TextField(db_column='end_date:note', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    start_date_edtf = models.TextField(db_column='start_date:edtf', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    source_operator = models.TextField(db_column='source:operator', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    operator_1940 = models.TextField(db_column='operator:1940', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    end_date_freight = models.TextField(db_column='end_date:freight', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    end_date_passengers = models.TextField(db_column='end_date:passengers', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    start_date_passengers = models.TextField(db_column='start_date:passengers', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1886_1937 = models.TextField(db_column='name:1886-1937', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1937_field = models.TextField(db_column='name:1937-', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    source_data = models.TextField(db_column='source:data', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1932_1934 = models.TextField(db_column='name:1932-1934', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    name_1881_1895 = models.TextField(db_column='name:1881-1895', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    start_date_source = models.TextField(db_column='start_date:source', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    wikimedia_commons = models.TextField(blank=True, null=True)
    station = models.TextField(blank=True, null=True)
    subway = models.TextField(blank=True, null=True)
    geometry = models.GeometryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osmhistory_rail_routes'


class OsmhistoryRailroutesGeojson(models.Model):
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    geometry = models.GeometryField(dim=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'osmhistory_railroutes.geojson'


class RttNaptanrailreferences(models.Model):
    atcocode = models.CharField(max_length=20, blank=True, null=True)
    tiploccode = models.CharField(max_length=20, blank=True, null=True)
    crscode = models.CharField(max_length=10, blank=True, null=True)
    stationname = models.CharField(max_length=100, blank=True, null=True)
    stationnamelang = models.CharField(max_length=2, blank=True, null=True)
    gridtype = models.CharField(max_length=1, blank=True, null=True)
    easting = models.IntegerField(blank=True, null=True)
    northing = models.IntegerField(blank=True, null=True)
    revisionnumber = models.SmallIntegerField(blank=True, null=True)
    modification = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rtt_naptanrailreferences'


class StorymapsSlide(models.Model):
    background = models.CharField(max_length=300, blank=True, null=True)
    northing = models.FloatField(blank=True, null=True)
    easting = models.FloatField(blank=True, null=True)
    zoom = models.SmallIntegerField()
    media_caption = models.CharField(max_length=100, blank=True, null=True)
    media_credit = models.CharField(max_length=200, blank=True, null=True)
    media_url = models.CharField(max_length=400, blank=True, null=True)
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storymaps_slide'


class StorymapsSlideheader(models.Model):
    location_line = models.BooleanField()
    media_caption = models.CharField(max_length=100, blank=True, null=True)
    media_credit = models.CharField(max_length=200, blank=True, null=True)
    media_url = models.CharField(max_length=300, blank=True, null=True)
    text_headline = models.CharField(max_length=200, blank=True, null=True)
    text_text = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'storymaps_slideheader'


class StorymapsSlidepack(models.Model):
    slide_order = models.SmallIntegerField()
    slide_fk = models.ForeignKey(StorymapsSlide, models.DO_NOTHING)
    slideheader_fk = models.ForeignKey(StorymapsSlideheader, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'storymaps_slidepack'


class ThumbnailKvstore(models.Model):
    key = models.CharField(primary_key=True, max_length=200)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'thumbnail_kvstore'


class VehiclesUklicensedvehicles(models.Model):
    year_ending = models.IntegerField()
    year_licensed = models.CharField(max_length=30)
    number_licensed = models.IntegerField()
    date_added = models.DateTimeField()
    make = models.ForeignKey('VehiclesVehiclemake', models.DO_NOTHING, blank=True, null=True)
    model = models.ForeignKey('VehiclesVehiclemodel', models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('VehiclesVehicletype', models.DO_NOTHING, blank=True, null=True)
    variant = models.ForeignKey('VehiclesVehiclevariant', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicles_uklicensedvehicles'


class VehiclesVehiclebmimage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    image = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehiclebmimage'


class VehiclesVehiclebmimageUsersLike(models.Model):
    vehiclebmimage = models.ForeignKey(VehiclesVehiclebmimage, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehiclebmimage_users_like'
        unique_together = (('vehiclebmimage', 'user'),)


class VehiclesVehicleimage(models.Model):
    image_name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    notes = models.TextField()
    date_added = models.DateTimeField()
    location = models.ForeignKey(MapsHeritagesite, models.DO_NOTHING)
    make = models.ForeignKey('VehiclesVehiclemake', models.DO_NOTHING)
    model = models.ForeignKey('VehiclesVehiclemodel', models.DO_NOTHING)
    visit = models.ForeignKey(MapsVisit, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehicleimage'


class VehiclesVehiclemake(models.Model):
    make = models.CharField(max_length=50)
    date_added = models.DateTimeField()
    type = models.ForeignKey('VehiclesVehicletype', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehiclemake'


class VehiclesVehiclemodel(models.Model):
    model = models.CharField(max_length=80)
    date_added = models.DateTimeField()
    make = models.ForeignKey(VehiclesVehiclemake, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehiclemodel'


class VehiclesVehicletype(models.Model):
    type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicles_vehicletype'


class VehiclesVehiclevariant(models.Model):
    variant = models.CharField(max_length=80)
    date_added = models.DateTimeField()
    model = models.ForeignKey(VehiclesVehiclemodel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'vehicles_vehiclevariant'
