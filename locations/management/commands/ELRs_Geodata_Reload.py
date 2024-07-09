"""
Reloads the Geodata and Geometry fields from a backup csv file of the ELR table
"""

from csv import DictReader
from django.core.management import BaseCommand
import os
from locations.models import *
from django.contrib.gis.geos import MultiLineString
from django.contrib.gis.geos import LineString

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


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
    help = "Loads Wikidata Engineer Line Reference Data"

    def handle(self, *args, **options):

        ELRs_updated = 0

        with open(
            os.path.join(DATAIO_DIR, "locations_elr.csv"), encoding="utf-8-sig"
        ) as file:

            for row in DictReader(file, delimiter="|"):
                print(row["id"])
                elrid = row["id"]
                elr = ELR.objects.get(id=elrid)
                try:
                    elr.geodata = row["geodata"]
                except Exception as e:
                    print(e)

                if row["geometry"] != "":
                    try:
                        # elr.geometry = row["geometry"]
                        elr.geometry = geojson_to_geometry(elr.geodata)
                    except Exception as e:
                        print(e)
                else:
                    elr.geometry = None
                elr.save()
                ELRs_updated += 1

        print(f"{ELRs_updated=}")
