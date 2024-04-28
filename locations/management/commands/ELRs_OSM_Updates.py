from django.core.management import BaseCommand
from locations.models import ELR

# from django.contrib.gis.geos import MultiLineString
# from django.contrib.gis.geos import LineString
from ...utils import osm_elr_fetch

"""
Translate OSM Geojson data into Postgres Geometry
Redundant as of 28/04/24 given that GeometryField on ELRS is not used by TPAM at present and has been removed to save space on the database (from 174 to 147Mb)
Also django.contriib.gis.geos was encountering errors in the conda GeoDjango environment
Retained here for potential future use
"""


def geojson_to_geometry(geojson):
    line_strings = []

    # Iterate through features and extract LineString geometries
    for feature in geojson["features"]:
        coordinates = feature["geometry"]["coordinates"]
        try:
            line_strings.append(LineString(coordinates))
        except Exception as e:
            print(f"When converting geojson to geometry had an exception of {e}")

    # Create a MultiLineString geometry from the list of LineStrings
    return MultiLineString(line_strings)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Updates one, one or more or all elr instances, with or without going to OpenRailMaps to get the geodata"

    def handle(self, *args, **options):

        update_all = True
        refresh_from_OSM = True
        refresh_geometry = False

        if update_all:
            elrs = ELR.objects.all()
        else:
            elrs = ["LCH"]

        for elr in elrs:
            if update_all == False:
                instance = ELR.objects.get(itemAltLabel=elr)
            else:
                instance = elr

            if refresh_from_OSM == True:
                instance.geodata = osm_elr_fetch(instance.itemAltLabel, None)
                instance.save()
                print(f"{instance.itemAltLabel} saved")

            try:
                if (
                    refresh_geometry
                    and instance.geodata
                    and len(instance.geodata["features"]) > 0
                ):
                    instance.geometry = geojson_to_geometry(instance.geodata)
                    instance.save()
                else:
                    print(f"{instance} has no geodata")
            except Exception as e:
                print(f"Error {e} on instance {instance}")
