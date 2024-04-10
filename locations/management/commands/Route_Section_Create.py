from django.core.management import BaseCommand
from locations.models import RouteSection, Route
from osm2geojson import json2geojson
from django.contrib.gis.geos import MultiLineString, LineString
from ...utils import osm_elr_fetch


class Command(BaseCommand):

    help = """
    Gets all RouteSections in the database, along with the associated Route and multiple ELRs. Then gets the geojson data for each ELR from OpenStreetMaps and applies any co-ordinate constraints on the RouteSection to reduce down that data, after which the data is saved to the RouteSection both as a geojson and as a geometry field. At the same time any dates for the route section are written onto every feature of the Geojson, though as at 14/02/24 this is not used in the TPAM app; this was done to show how in the future the same could be applied to ELR geodata so that they could be searched for dates, rather than the geojsons having to be reduced/duplicated onto the RouteSection geodata.
    """

    def handle(self, *args, **options):
        instances = RouteSection.objects.all()
        for instance in instances:

            instance.geodata = None
            instance.geometry = None

            route = Route.objects.get(slug="Brighton_to_Portsmouth_line")
            instance.route_fk = route

            route_section_elrs = instance.routesectionelr_set.all()

            elrs_geojsons = None
            if route_section_elrs:
                for elr in route_section_elrs:
                    min_lat = elr.min_lat or 49
                    min_lon = elr.min_lon or -7
                    max_lat = elr.max_lat or 59
                    max_lon = elr.max_lon or 2
                    elr_geojson = osm_elr_fetch(
                        elr.elr_fk.itemAltLabel, (min_lat, min_lon, max_lat, max_lon)
                    )

                    if elr_geojson:
                        elrs_geojsons = (
                            elrs_geojsons or []
                        )  # If first geojson convert elr_geojsons from None to List
                        elrs_geojsons.append(elr_geojson)

            if elrs_geojsons:

                line_strings = []
                for geojson in elrs_geojsons:

                    # Iterate through features and extract LineString geometries

                    for feature in geojson["features"]:
                        coordinates = feature["geometry"]["coordinates"]

                        # Here we write the dates onto all features
                        if "properties" in feature:
                            properties = feature["properties"]
                        else:
                            properties = {}

                        # Check if the "tags" field exists
                        if "tags" in properties:
                            tags = properties["tags"]
                        else:
                            tags = {}

                        # Add or update the value of the "opened" field
                        tags["opened"] = instance.date_opened
                        tags["closed"] = instance.date_closed
                        tags["opened_passenger"] = instance.date_opened_passenger
                        tags["closed_passenger"] = instance.date_closed_passenger

                        # Update the "tags" field within "properties"
                        properties["tags"] = tags

                        # Update the "properties" field within the main data
                        feature["properties"] = properties

                        try:
                            line_strings.append(LineString(coordinates))
                        except Exception as e:
                            print(f"{instance} had an exception of {e}")

                    # Create a MultiLineString geometry from the list of LineStrings
                instance.geometry = MultiLineString(line_strings)

            instance.geodata = elrs_geojsons
            instance.save()
