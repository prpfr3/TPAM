from csv import DictReader
from urllib.parse import unquote
from django.core.management import BaseCommand
from locations.models import Route, RouteCategory, RouteMap
import os

DATAIO_DIR = os.path.join("C:\\Users\\paulf\\OneDrive\\Data", "TPAM")


class Command(BaseCommand):
    help = "Deletes Route data loaded by Routes_W2_Load"

    def handle(self, *args, **options):
        deleted_routes = 0
        route_map_names = set()
        category_names = set()

        with open(
            os.path.join(DATAIO_DIR, "Routes_Switzerland.csv"), encoding="utf-8"
        ) as file:
            for row in DictReader(file):
                wikislug = unquote(row["wikislug"].encode("utf-8"))
                wikislug = wikislug.replace("/wiki/","")
                routes = Route.objects.filter(wikipedia_slug=wikislug)
                route_count = routes.count()
                if route_count:
                    deleted_routes += route_count
                    routes.delete()
                    self.stdout.write(f"Deleted {route_count} route(s) for {wikislug}")
                else:
                    self.stdout.write(f"No route found for {wikislug}")

                if row.get("routemap"):
                    routemap_name = unquote(row["routemap"].encode("utf-8"))
                    route_map_names.add(routemap_name)

                if row.get("category"):
                    wikipedia_category = row["category"].replace("_", " ")
                    wikipedia_category = wikipedia_category.replace(
                        "https://en.wikipedia.org/wiki/Category:", ""
                    )
                    category_names.add(wikipedia_category)

        deleted_route_maps = 0
        for name in route_map_names:
            for route_map in RouteMap.objects.filter(name=name):
                if not route_map.route_set.exists():
                    route_map.delete()
                    deleted_route_maps += 1
                    self.stdout.write(f"Deleted orphan RouteMap {name}")

        deleted_categories = 0
        for category in category_names:
            for route_category in RouteCategory.objects.filter(category=category):
                if not route_category.route_set.exists():
                    route_category.delete()
                    deleted_categories += 1
                    self.stdout.write(f"Deleted orphan RouteCategory {category}")

        self.stdout.write(
            f"Finished: deleted {deleted_routes} route(s), {deleted_route_maps} orphan route map(s), {deleted_categories} orphan route category(ies)."
        )
