# Extracts a list of sheds from Wikipedia and loads into the TPAM database

import os
from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
INPUTFILE = "Depots_Wikipedia_Links.csv"


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(os.path.join(DATAIO_DIR, INPUTFILE), encoding="utf-8-sig") as file:
            for row in DictReader(file):
                try:
                    depot = Location.objects.get(name=row["name"])
                    depot.wikislug = row["wikislug"]
                    depot.save()
                    print(f"Updated {depot.name} with wikislug of {depot.wikislug}")
                except Exception as e:
                    print(depot.name, e)
