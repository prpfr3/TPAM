from notes.models import *
from companies.models import Company

# from django.contrib.gis.db import models
from django.db import models


class Depot(models.Model):
    depot = models.CharField(max_length=1000, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    date_start = models.CharField(max_length=10, blank=True, null=True)
    datefield_start = models.DateField(blank=True, null=True)
    date_end = models.CharField(max_length=10, blank=True, null=True)
    datefield_end = models.DateField(blank=True, null=True)
    br_region = models.CharField(
        db_column="BR_region", max_length=20, blank=True, null=True
    )
    map = models.CharField(max_length=200, blank=True, null=True)
    web = models.CharField(max_length=200, blank=True, null=True)
    comments = models.TextField()
    image = models.ImageField(upload_to="images/", default=None)

    class Meta:
        verbose_name = "Depot"
        verbose_name_plural = "Depots"


class ELR(models.Model):
    item = models.SlugField(max_length=20, blank=True, default="")
    itemLabel = models.CharField(max_length=400, blank=True, default="")
    itemAltLabel = models.CharField(max_length=200, blank=True, default="")
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )

    def __str__(self):
        return f"{self.itemAltLabel} {self.itemLabel}" or ""

    class Meta:
        verbose_name = "Engineer's Line Reference"
        verbose_name_plural = "Engineer's Line References"


class Location(models.Model):
    SOURCE_TYPE = (
        (1, "Wikipedia"),
        (2, "Custom"),
    )

    type = models.CharField(max_length=20, blank=True, null=True)
    wikiname = models.CharField(max_length=200, blank=True, null=True)
    wikislug = models.CharField(max_length=250, default=None, blank=True, null=True)
    postcode = models.CharField(default=None, blank=True, null=True, max_length=10)
    opened = models.CharField(max_length=200, blank=True, null=True)
    closed = models.CharField(max_length=200, blank=True, null=True)
    disused_stations_slug = models.CharField(max_length=200, blank=True, null=True)
    # Geometry Field if using contrib.gis
    geometry = models.TextField(blank=True, null=True)
    atcocode = models.CharField(max_length=20, blank=True, null=True)
    tiploccode = models.CharField(max_length=20, blank=True, null=True)
    crscode = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    namealt = models.CharField(max_length=100, blank=True, null=True)
    namelang = models.CharField(max_length=2, blank=True, null=True)
    gridtype = models.CharField(max_length=1, blank=True, null=True)
    easting = models.PositiveIntegerField(blank=True, null=True)
    northing = models.PositiveIntegerField(blank=True, null=True)
    creationdatetime = models.DateTimeField
    modificationdatetime = models.DateTimeField
    revisionnumber = models.SmallIntegerField(blank=True, null=True)
    modification = models.CharField(max_length=3, blank=True, null=True)
    elr_points = models.ManyToManyField(
        ELR, through="ELRLocation", blank=True, related_name="elr_locations"
    )
    elr_fk = models.ForeignKey(
        ELR, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    osm_node = models.CharField(max_length=20, blank=True, null=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    references = models.ManyToManyField(Reference, blank=True)
    source = models.IntegerField(
        choices=SOURCE_TYPE,
        default=1,
    )
    media_caption = models.CharField(max_length=100, blank=True, null=True)
    media_credit = models.CharField(max_length=200, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True, max_length=400)

    def get_absolute_url(self):
        # Enables "View on Site" link in Admin to go to detail view on (non-admin) site
        from django.urls import reverse

        return reverse("locations:location", kwargs={"location_id": self.pk})

    def __str__(self):
        return self.wikiname or self.name or str(self.id)

    class Meta:
        managed = False


class RouteCategory(models.Model):
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Route Category"
        verbose_name_plural = "Route Categories"
        managed = True


class RouteMap(models.Model):
    # In Wikipedia, a Routemap can appear on more than one Route page.
    SOURCE_TYPE = (
        (1, "Wikipedia"),
        (2, "Custom"),
    )
    name = models.CharField(max_length=1000, null=True)
    source = models.IntegerField(
        choices=SOURCE_TYPE,
        default=1,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Route Map"
        verbose_name_plural = "Route Maps"
        managed = True


class Route(models.Model):
    SOURCE_TYPE = (
        (1, "Wikipedia"),
        (2, "Custom"),
    )
    name = models.CharField(max_length=1000, blank=True, default="")
    wikipedia_slug = models.SlugField(
        default=None, allow_unicode=True, null=True, max_length=255
    )
    wikipedia_categories = models.ManyToManyField(RouteCategory, blank=True)
    wikipedia_routemaps = models.ManyToManyField(RouteMap, blank=True)
    elrs = models.ManyToManyField(ELR, blank=True)
    references = models.ManyToManyField(Reference, blank=True)
    post_fk = models.ForeignKey(
        Post, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )
    owneroperators = models.ManyToManyField(Company, blank=True)
    source = models.IntegerField(
        choices=SOURCE_TYPE,
        default=1,
    )

    def __str__(self):
        return self.name


class RouteLocation(models.Model):
    routemap = models.ForeignKey(RouteMap, on_delete=models.CASCADE, default=1)
    loc_no = models.IntegerField()
    label = models.CharField(max_length=1000, blank=True, null=True)
    location_fk = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    linear_reference = models.DecimalField(
        blank=True, null=True, default=None, max_digits=6, decimal_places=2
    )
    note = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Route Location"
        verbose_name_plural = "Route Locations"


class ELRLocation(models.Model):
    location_fk = models.ForeignKey(Location, on_delete=models.CASCADE)
    elr_fk = models.ForeignKey(ELR, blank=True, null=True, on_delete=models.CASCADE)
    distance = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f" {self.location_fk.__str__} {self.elr_fk.__str__}"

    class Meta:
        verbose_name = "Engineer's Line Reference Location"
        verbose_name_plural = "Engineer's Line Reference Locations"


class LocationEvent(models.Model):
    EVENT_TYPE = (
        (1, "Official Opening"),
        (2, "Closed to Passengers"),
        (3, "Closed to Freight"),
        (4, "Razed"),
        (5, "Name Change"),
        (99, "Other"),
    )
    type = models.IntegerField(
        choices=EVENT_TYPE,
        default=1,
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    datefield = models.DateField(blank=True, null=True)
    route_fk = models.ForeignKey(
        Route, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    location_fk = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    elr_fk = models.ForeignKey(
        ELR, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    location_description = models.CharField(
        max_length=100, blank="True", null="True", default=None
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.get_type_display())}: {str(self.description)}"

    class Meta:
        verbose_name = "Location Event"
        verbose_name_plural = "Location Events"


"""
CLOSED RAILWAY DATA FROM GOOGLE MAPS
"""


class RouteGeoClosed(models.Model):
    # Field name made lowercase. Had to change Name to name in PgAdmin
    name = models.TextField(db_column="name", blank=True, null=True)
    # Field name made lowercase.
    description = models.TextField(db_column="Description", blank=True, null=True)
    # Geometry Field if using contrib.gis
    geometry = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "locations_routes_geo_closed"
        verbose_name = "Closed Route Geometries"
        verbose_name_plural = "Closed Routes Geometries"

    def __str__(self):
        return self.name


"""
RAILWAYS DATA FROM OSM
To recreate and populate this model
Load the data via OSM_GoogleMaps_dataloads.ipynb
Then generate the Django table model from the loaded database table using:-
  python manage.py inspectdb > models_temporary.py
Then copy the model from models_temporary.py to here

Convert the id field to null=False, primary_key=True 
(note the id field already exists in the loaded data but does contain characters)
"""


class RouteGeoOsm(models.Model):
    id = models.TextField(blank=True, null=False, primary_key=True)
    # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_id = models.TextField(db_column="@id", blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    from_field = models.TextField(db_column="from", blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_de = models.TextField(db_column="name:de", blank=True, null=True)
    network = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    network_wikidata = models.TextField(
        db_column="network:wikidata", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    network_wikipedia = models.TextField(
        db_column="network:wikipedia", blank=True, null=True
    )
    operator = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    public_transport_version = models.TextField(
        db_column="public_transport:version", blank=True, null=True
    )
    ref = models.TextField(blank=True, null=True)
    route = models.TextField(blank=True, null=True)
    service = models.TextField(blank=True, null=True)
    to = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    bicycle = models.TextField(blank=True, null=True)
    by_night = models.TextField(blank=True, null=True)
    colour = models.TextField(blank=True, null=True)
    dining = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    from_de = models.TextField(db_column="from:de", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    from_fr = models.TextField(db_column="from:fr", blank=True, null=True)
    highspeed = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_en = models.TextField(db_column="name:en", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_fr = models.TextField(db_column="name:fr", blank=True, null=True)
    reservation = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    to_fr = models.TextField(db_column="to:fr", blank=True, null=True)
    via = models.TextField(blank=True, null=True)
    wheelchair = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.TextField(blank=True, null=True)
    tt_ref = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    srs = models.TextField(db_column="SRS", blank=True, null=True)
    electrified = models.TextField(blank=True, null=True)
    freight_gauge = models.TextField(blank=True, null=True)
    interval = models.TextField(blank=True, null=True)
    line_classification = models.TextField(blank=True, null=True)
    strategic_route = models.TextField(blank=True, null=True)
    wikidata = models.TextField(blank=True, null=True)
    wikipedia = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    colour_infill = models.TextField(db_column="colour:infill", blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    ref_colour = models.TextField(db_column="ref:colour", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    ref_colour_bg = models.TextField(db_column="ref:colour_bg", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    ref_colour_tx = models.TextField(db_column="ref:colour_tx", blank=True, null=True)
    text_colour = models.TextField(blank=True, null=True)
    tracks = models.TextField(blank=True, null=True)
    voltage = models.TextField(blank=True, null=True)
    railway = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    source_ref = models.TextField(db_column="source:ref", blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    monorail = models.TextField(blank=True, null=True)
    opening_hours = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    operator_cy = models.TextField(db_column="operator:cy", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    operator_en = models.TextField(db_column="operator:en", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    note_colour = models.TextField(db_column="note:colour", blank=True, null=True)
    official_ref = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    operator_wikidata = models.TextField(
        db_column="operator:wikidata", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    operator_wikipedia = models.TextField(
        db_column="operator:wikipedia", blank=True, null=True
    )
    line = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_cy = models.TextField(db_column="name:cy", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_nl = models.TextField(db_column="name:nl", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    to_de = models.TextField(db_column="to:de", blank=True, null=True)
    old_ref = models.TextField(blank=True, null=True)
    fee = models.TextField(blank=True, null=True)
    headway = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    not_network_wikidata = models.TextField(
        db_column="not:network:wikidata", blank=True, null=True
    )
    website = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_oc = models.TextField(db_column="name:oc", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    source_name_oc = models.TextField(db_column="source:name:oc", blank=True, null=True)
    passenger = models.TextField(blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)
    distance = models.TextField(blank=True, null=True)
    maxwidth = models.TextField(blank=True, null=True)
    roundtrip = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    wikipedia_en = models.TextField(db_column="wikipedia:en", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    from_nl = models.TextField(db_column="from:nl", blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    ref_prorail = models.TextField(db_column="ref:ProRail", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    to_nl = models.TextField(db_column="to:nl", blank=True, null=True)
    bus = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cargo_bus = models.TextField(db_column="cargo:bus", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    cargo_vehicle = models.TextField(db_column="cargo:vehicle", blank=True, null=True)
    motor_vehicle = models.TextField(blank=True, null=True)
    segment = models.TextField(blank=True, null=True)
    internet_access = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    internet_access_fee = models.TextField(
        db_column="internet_access:fee", blank=True, null=True
    )
    surveillance = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    surveillance_type = models.TextField(
        db_column="surveillance:type", blank=True, null=True
    )
    historic = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_relations = models.TextField(db_column="@relations", blank=True, null=True)
    # Geometry Field if using contrib.gis
    geometry = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "locations_routes_geo_osm"
        verbose_name = "OSM Route Geometry"
        verbose_name_plural = "OSM Routes Geometries"

    def __str__(self):
        return self.id


"""
RAILWAY DATA FROM OSM HISTORY
Load the data via OSM_GoogleMaps_dataloads.ipynb
Then generate the Django table model from the loaded database table using:-
  python manage.py inspectdb > models_temporary.py
Then copy the model from models_temporary.py to here

Convert the id field to null=False, primary_key=True 
(note the id field already exists in the loaded data but does contain characters)
"""


class RouteGeoOsmhistory(models.Model):
    id = models.TextField(blank=True, null=False, primary_key=True)
    # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_id = models.TextField(db_column="@id", blank=True, null=True)
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
    # Field renamed to remove unsuitable characters.
    start_date_note = models.TextField(
        db_column="start_date:note", blank=True, null=True
    )
    area = models.TextField(blank=True, null=True)
    end_date = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    building_levels = models.TextField(
        db_column="building:levels", blank=True, null=True
    )
    structure = models.TextField(blank=True, null=True)
    landuse = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1863_1908 = models.TextField(db_column="name:1863-1908", blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1848_1966 = models.TextField(db_column="name:1848-1966", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1966_2021 = models.TextField(db_column="name:1966-2021", blank=True, null=True)
    architect = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    architect_wikipedia = models.TextField(
        db_column="architect:wikipedia", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    name_1847_1922 = models.TextField(db_column="name:1847-1922", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1922 = models.TextField(db_column="name:1922", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    company_1898 = models.TextField(db_column="company:1898", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    company_end = models.TextField(db_column="company:end", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    company_start = models.TextField(db_column="company:start", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    end_date_goods = models.TextField(db_column="end_date:goods", blank=True, null=True)
    gauge = models.TextField(blank=True, null=True)
    # Field name made lowercase. Field renamed to remove unsuitable characters.
    start_date_gwr = models.TextField(db_column="start_date:GWR", blank=True, null=True)
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
    # Field renamed to remove unsuitable characters.
    start_date_source = models.TextField(
        db_column="start_date:source", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    start_date_edtf = models.TextField(
        db_column="start_date:edtf", blank=True, null=True
    )
    electrified = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    end_date_edtf = models.TextField(db_column="end_date:edtf", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    end_date_note = models.TextField(db_column="end_date:note", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    source_operator = models.TextField(
        db_column="source:operator", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    operator_1940 = models.TextField(db_column="operator:1940", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    end_date_freight = models.TextField(
        db_column="end_date:freight", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    end_date_passengers = models.TextField(
        db_column="end_date:passengers", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    start_date_passengers = models.TextField(
        db_column="start_date:passengers", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    start_date_goods = models.TextField(
        db_column="start_date:goods", blank=True, null=True
    )
    # Field renamed to remove unsuitable characters.
    name_1886_1937 = models.TextField(db_column="name:1886-1937", blank=True, null=True)
    # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    name_1937_field = models.TextField(db_column="name:1937-", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    source_data = models.TextField(db_column="source:data", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1932_1934 = models.TextField(db_column="name:1932-1934", blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    name_1881_1895 = models.TextField(db_column="name:1881-1895", blank=True, null=True)
    wikimedia_commons = models.TextField(blank=True, null=True)
    station = models.TextField(blank=True, null=True)
    subway = models.TextField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    railway_yard_purpose = models.TextField(
        db_column="railway:yard:purpose", blank=True, null=True
    )
    # Geometry Field if using contrib.gis
    geometry = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "locations_routes_geo_osmhistory"
        managed = False
        verbose_name = "OSM History Route Geometry"
        verbose_name_plural = "OSM History Routes Geometries"


class UkAdminBoundaries(models.Model):
    objectid = models.CharField(max_length=10, null=False, primary_key=True)
    ctyua19cd = models.CharField(max_length=100, blank=True, null=True)
    ctyua19nm = models.CharField(max_length=100, blank=True, null=True)
    ctyua19nmw = models.CharField(max_length=100, blank=True, null=True)
    bng_e = models.FloatField(blank=True, null=True)
    bng_n = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    st_areasha = models.FloatField(blank=True, null=True)
    st_lengths = models.FloatField(blank=True, null=True)
    # Geometry Field if using contrib.gis
    geometry = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "locations_UK_admin_boundaries"
        verbose_name = "UK Admin Area Geometry"
        verbose_name_plural = "UK Admin Areas Geometries"

    def __str__(self):
        return self.ctyua19nm


class HeritageSite(models.Model):
    tpam_type = models.ForeignKey(
        "mainmenu.MyDjangoApp",
        default=1,
        verbose_name="Heritage Site Type",
        on_delete=models.SET_DEFAULT,
    )
    type = models.CharField(max_length=50, default=None, blank=True)
    name = models.CharField(max_length=100, default=None, blank=True)
    country = models.CharField(max_length=100, default=None, blank=True)
    wikislug = models.SlugField(
        max_length=250, allow_unicode=True, default=None, blank=True, null=True
    )
    url = models.URLField(default=None, blank=True, null=True)
    notes = models.TextField(default=None, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Visit(models.Model):  # Visit to a Location / Heritage Site
    location = models.ForeignKey(
        HeritageSite,
        default=1398,
        verbose_name="Location",
        on_delete=models.SET_DEFAULT,
    )
    date = models.DateField(blank=True)
    notes = models.TextField(default=None, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)
