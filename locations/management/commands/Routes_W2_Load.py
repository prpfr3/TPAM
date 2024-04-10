from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Route, RouteCategory, RouteMap
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    help = "Loads Route Data"

    def handle(self, *args, **options):
        if Route.objects.exists():
            print("Route data already loaded...but continuing with load.")
        else:
            print("Creating Routes")

        routes_added = 0
        route_templates_added = 0
        route_category_created = 0

        with open(
            os.path.join(DATAIO_DIR, "Routes_Manual_Additions.csv"), encoding="utf-8"
        ) as file:
            for row in DictReader(file):
                from urllib.parse import unquote

                wikislug = unquote(row["wikislug"].encode("utf-8"))
                route_fk, route_created = Route.objects.get_or_create(
                    name=row["name"], wikipedia_slug=wikislug
                )
                if route_created:
                    routes_added += 1

                # Get or create the routemap for the route and then add the routemap as a fk into the route table
                if row["routemap"] != None:
                    wikipedia_routemap = unquote(row["routemap"].encode("utf-8"))
                    wikipedia_routemap = wikipedia_routemap
                    routemap, routemap_created = RouteMap.objects.get_or_create(
                        name=wikipedia_routemap,
                    )
                    if route_fk.wikipedia_routemaps.filter(id=routemap.id):
                        print("Routemap already associated with the route")
                    else:
                        route_fk.wikipedia_routemaps.add(routemap)
                        print("Routemap added to the route")
                    if routemap_created:
                        route_templates_added += 1
                    route_fk.wikipedia_routemaps.add(routemap)

                # Get or create the route category for the route and then add the category as a fk into the route table
                wikipedia_category = row["category"]
                wikipedia_category = wikipedia_category.replace("_", " ")
                wikipedia_category = wikipedia_category.replace(
                    "https://en.wikipedia.org/wiki/Category:", ""
                )
                category_fk, category_created = RouteCategory.objects.get_or_create(
                    category=wikipedia_category,
                )
                if category_created:
                    route_category_created += 1
                route_fk.categories.add(category_fk)

        print(
            f"{routes_added=}, {route_templates_added=} and {route_category_created=}"
        )
