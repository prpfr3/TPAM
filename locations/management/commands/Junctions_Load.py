from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location, LocationCategory

"""
Junctions can be categorised in OSM in two ways and hence two queries are required in Overpass Turbo:-

[out:csv(::id,::lat,::lon,"name")];
area["ISO3166-1"="GB"][admin_level=2];
node(area)["railway"="junction"];
out geom;
>;
out skel qt;

[out:csv(::id,::lat,::lon,"name")];
area["ISO3166-1"="GB"][admin_level=2];
node(area)["historic:railway"="junction"];
out geom;
>;
out skel qt;
"""

input_filename = "D://Data/TPAM/Location_Junctions_OSM_Historic.csv"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Wikidata file into the locations table"

    def handle(self, *args, **options):
        print("Loading Junctions")

        category = LocationCategory.objects.get(category="Junction")
        count = 0

        with open(input_filename, encoding="utf-8-sig") as csvfile:
            for row in DictReader(csvfile):
                Location.objects.filter(osm_node=row["@id"]).delete()
                l = Location()
                l, _ = Location.objects.get_or_create(osm_node=row["@id"])
                if category not in l.categories.all():
                    l.categories.add(category)
                l.geometry = f"POINT ({row['@lon']} {row['@lat']})"
                l.name = row["name"]
                # l.namealt = row["alt_name"]
                l.osm_node = row["@id"]
                l.save()
                count += 1

        print(f"{count} junctions loaded as locations")
