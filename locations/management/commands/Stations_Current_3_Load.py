import os
from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand
from locations.models import Location, LocationCategory


class Command(BaseCommand):

    def handle(self, *args, **options):

        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        current_date = datetime.now().strftime("%Y-%m-%d")
        INPUT_LOADFILE = os.path.join(
            DATAIO_DIR,
            f"Location_Stations_Current_Loadfile_{current_date}.csv",
        )

        print("Creating Locations")
        if Location.objects.exists():
            print("Note there is already data in the table")

        count = 0

        for row in DictReader(open(INPUT_LOADFILE)):
            if count != 0 and row["CrsCode"] != "":
                locations = Location.objects.filter(wikislug=row["NameSlug"])

                if locations.exists():
                    for l in locations:
                        self.update_location(l, row)
                else:
                    l = Location()
                    self.update_location(l, row, new=True)
                    print(f"New location created for {row} ")

            count += 1

        print(f"{count} railway station locations loaded/amended")

    def update_location(self, location, row, new=False):
        if new:
            location.wikislug = row["NameSlug"]

        # Retrieve key of "Current Station" Category
        current_station_category = LocationCategory.objects.get(
            category="Current Station"
        )

        # Check if this category is associated with the current location
        try:
            if current_station_category.id:
                if not location.categories.filter(
                    id=current_station_category.id
                ).exists():
                    location.categories.add(current_station_category)
                    print(
                        f"New entry added to the LocationCategories table for {location}"
                    )
        except Exception as e:
            print(f"Error {e} for location {location.id}")

        location.wikiname = row["Name"]
        location.postcode = row["Postcode"]
        location.geometry = row["geometry"]
        location.atcocode = row["AtcoCode"]
        location.tiploccode = row["TiplocCode"]
        location.crscode = row["CrsCode"]
        location.name = row["StationName"]
        if row["Easting"] != "":
            location.easting = row["Easting"]
            location.northing = row["Northing"]
        else:
            location.easting = None
            location.northing = None
        try:
            location.save()
        except Exception as e:
            print(f"Error {e} for {location.name}")
