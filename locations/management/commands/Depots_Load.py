# Extracts a list of sheds from Wikipedia and loads into the TPAM database

import os
from csv import DictReader

from django.core.management import BaseCommand
from locations.models import Location, LocationCategory
from OSGridConverter import grid2latlong

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUTFILE = "Depots_Cleansed.csv"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data a manually cleansed file of depots into the Depot table"

    def handle(self, *args, **options):
        if Location.objects.exists():
            print("Depot data already exists but continuing.")
        else:
            print("Creating Depots for the first time")

        category_4, _ = LocationCategory.objects.get_or_create(id=4)

        with open(os.path.join(DATAIO_DIR, INPUTFILE), encoding="utf-8-sig") as file:
            for row in DictReader(file):
                depot = Location()
                depot, _ = Location.objects.get_or_create(name=row["name"])

                depot.name = row["name"]

                # Check if the Location is associated with the required category 4
                if category_4 not in depot.categories.all():
                    # If not, associate the Location with category 4
                    depot.categories.add(category_4)

                depot.opened = row["opened"]
                depot.closed = row["closed"]
                depot.closed_to_steam = row["closed to steam"]
                if row["coordinates"]:
                    l = grid2latlong(row["coordinates"])
                    depot.northing = l.latitude
                    depot.easting = l.longitude
                from django.contrib.gis.geos import Point

                if depot.easting is not None and depot.northing is not None:
                    srid = 4326
                    point = Point(depot.easting, depot.northing, srid=srid)
                    depot.geometry = point

                depot.save()
