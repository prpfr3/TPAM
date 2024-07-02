from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location, LocationCategory
import contextlib

input_filename = "D://Data/TPAM/Location_Tunnels_Wikidata_2024-06-26.csv"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Wikidata file into the locations table"

    def handle(self, *args, **options):
        print("Loading Tunnels")

        category = LocationCategory.objects.get(category="Tunnel")
        count = 0

        with open(input_filename, encoding="utf-8-sig") as csvfile:
            for row in DictReader(csvfile):
                l = Location()
                l, _ = Location.objects.get_or_create(name=row["item"][31:])
                if category not in l.categories.all():
                    # If not, associate the Location with category 4
                    l.categories.add(category)
                l.geometry = row["geo"]
                l.name = row["itemLabel"]
                l.wikislug = row["wikipediaSlug"].replace(" ", "_")
                l.save()
                count += 1

        print(f"{count} tunnels loaded as locations")
