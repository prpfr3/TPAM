# Extracts a list of sheds from Wikipedia and loads into the TPAM database

import os
import requests
import datetime
import pandas as pd
from csv import DictReader

from django.core.management import BaseCommand
from locations.models import Location, LocationCode

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUTFILE = "Depots_Cleansed.csv"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Depot Codes"

    def handle(self, *args, **options):
        if LocationCode.objects.exists():
            print("Depot codes data already exists but continuing.")
        else:
            print("Creating Depot Codes for the first time")

        with open(os.path.join(DATAIO_DIR, INPUTFILE), encoding="utf-8-sig") as file:
            for row in DictReader(file):
                if row["from_date"]:
                    instance = LocationCode()
                    instance.location_fk, _ = Location.objects.get_or_create(
                        name=row["name"]
                    )
                    instance.location_code = row["code"]
                    instance.from_date = row["from_date"]
                    instance.to_date = row["to_date"]
                    instance.save()
