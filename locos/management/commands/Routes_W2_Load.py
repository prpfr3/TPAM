from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Route, RouteCategory, RouteMap
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads Route Data"

    def handle(self, *args, **options):
        if Route.objects.exists():
            print('Route data already loaded...but continuing with load.')
        else:
            print("Creating Routes")
        with open(os.path.join(DATAIO_DIR, "Routes_All_W1.csv"), encoding="utf-8") as file: 
            for row in DictReader(file):                             
                route_fk, route_created = Route.objects.get_or_create(
                    name=row['name'],
                    wikipedia_slug = row['wikislug'],
                    )

                # Get or create the routemap for the route and then add the routemap as a fk into the route table
                if row['routemap'] != "":
                    wikipedia_routemap = row['routemap']
                    wikipedia_routemap = wikipedia_routemap.replace('/wiki/Template:', '')
                    routemap_fk, routemap_created = RouteMap.objects.get_or_create(name=wikipedia_routemap,) 
                    route_fk.wikipedia_routemaps.add(routemap_fk)

                # Get or create the route category for the route and then add the category as a fk into the route table
                wikipedia_category = row['category']
                wikipedia_category = wikipedia_category.replace('_', ' ')
                wikipedia_category = wikipedia_category.replace('https://en.wikipedia.org/wiki/Category:', '')
                category_fk, category_created = RouteCategory.objects.get_or_create(category=wikipedia_category,)             
                route_fk.wikipedia_route_categories.add(category_fk)