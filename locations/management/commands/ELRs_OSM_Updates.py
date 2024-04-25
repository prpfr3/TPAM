from django.core.management import BaseCommand
from locations.models import ELR
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos import LineString
from ...utils import osm_elr_fetch


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

        if update_all:
            elrs = ELR.objects.all()
        else:
            elrs = ["RDG1", "RDG2"]

        for elr in elrs:
            if update_all == False:
                instance = ELR.objects.get(itemAltLabel=elr)
            else:
                instance = elr

            if refresh_from_OSM == True and instance.geodata == None:
                instance.geodata = osm_elr_fetch(instance.itemAltLabel, None)

            try:
                if (
                    instance.geodata
                    and instance.geometry == None
                    and len(instance.geodata["features"]) > 0
                ):
                    instance.geometry = geojson_to_geometry(instance.geodata)
                    instance.save()
                else:
                    print(f"{instance} has no geodata")
            except Exception as e:
                print(f"Error {e} on instance {instance}")
