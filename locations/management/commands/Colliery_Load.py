from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location, LocationCategory

input_filename = "C:\\Users\\paulf\\OneDrive\\Data\\TPAM\\Somerset_Quarries.csv"

def build_geometry(latitude, longitude, fallback=""):
    lat = (latitude or "").strip()
    lon = (longitude or "").strip()

    if not lat or not lon:
        return fallback

    try:
        lat_value = float(lat)
        lon_value = float(lon)
    except ValueError:
        return fallback

    if not (-90 <= lat_value <= 90 and -180 <= lon_value <= 180):
        return fallback

    return f"POINT ({lon_value} {lat_value})"


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from Wikidata file into the locations table"

    def handle(self, *args, **options):
        print("Loading Quarries")

        category = LocationCategory.objects.get(category="Quarries")
        count = 0

        with open(input_filename, encoding="utf-8-sig") as csvfile:
            for row in DictReader(csvfile):
                name = (row.get("Name") or "").strip()
                if not name:
                    self.stderr.write("Skipping row with missing name")
                    continue

                l, _ = Location.objects.get_or_create(name=name)
                if category not in l.categories.all():
                    l.categories.add(category)

                latitude = row.get("Latitude")
                longitude = row.get("Longitude")
                geometry = build_geometry(latitude, longitude, fallback=row.get("geo", ""))
                if not geometry:
                    self.stderr.write(f"Skipping {name}: no valid coordinates or geo fallback")
                    continue

                l.name = name
                l.geometry = geometry
                l.notes = row.get("Description", "")
                opening_year = row.get("Opening", "")
                closing_year = row.get("Closing", "")

                wikipedia_slug = (row.get("wikipediaSlug") or "").strip()
                l.wikislug = wikipedia_slug.replace(" ", "_") if wikipedia_slug else ""
                l.save()
                count += 1

        print(f"{count} quarries loaded as locations")
