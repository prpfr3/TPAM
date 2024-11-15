"""
Reloads the Geojson fields from a backup csv file of the ELR table

Backup file can be created from Postgres Pgadmin by downloading the table to a csv file
"""

from django.core.management import BaseCommand
import os, csv
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

    def handle(self, *args, **options):

        cwd = os.getcwd()
        if cwd == "/app" or cwd.startswith("/home"):
            DATAIO_DIR = os.path.join("/home", "/django")
        else:
            DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

        input_file = os.path.join(DATAIO_DIR, "ELR_geojsons.csv")

        with open(input_file, encoding="utf-8-sig") as file:

            csv.field_size_limit(100 * 1024 * 1024)

            count = 0

            for row in csv.DictReader(file, delimiter="|"):

                elrid = row["id"]
                elr = ELR.objects.get(id=elrid)

                if row["geojson"] and count < 1:
                    count = count + 1

                    try:
                        elr.geojson = row["geojson"]
                    except Exception as e:
                        print(f"EXCEPTION {e} for record {elrid}")

                    try:
                        elr.save()
                    except Exception as e:
                        print(f"EXCEPTION on save of {e} for record {elrid}")

            self.stdout.write(f"{count} Geojsons reloaded to the ELR Table")
