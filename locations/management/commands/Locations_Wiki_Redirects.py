from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Location
import os


class Command(BaseCommand):
    help = "Adjusts Locations based on csv input"

    def handle(self, *args, **options):

        print("Making Adjustments")
        DATAIO_DIR = r"C:\Users\paulf\OneDrive\Data\TPAM"

        csv_path = os.path.join(DATAIO_DIR, "Locations_Wikipedia_Redirects.csv")

        with open(csv_path, encoding="utf-8-sig") as file:
            for row in DictReader(file):

                # --- Fetch original location ----------------------------------
                try:
                    l = Location.objects.get(id=row["id"])
                except Location.DoesNotExist:
                    print(f"No database entry for CSV row with id={row['id']}")
                    continue
                except Exception as e:
                    print(f"Error retrieving id={row['id']}: {e}")
                    continue

                # --- Fetch redirect target location ---------------------------
                try:
                    t = Location.objects.get(wikislug=row["target_slug"])
                except Location.DoesNotExist:
                    print(
                        f"Target wikislug '{row['target_slug']}' not found "
                        f"(from id={row['id']})"
                    )
                    continue
                except Exception as e:
                    print(f"Error retrieving target for id={row['id']}: {e}")
                    continue

                # --- Update alt names safely ----------------------------------
                w = row["wikiname"]
                if t.wiki_altnames:
                    t.wiki_altnames = f"{t.wiki_altnames}; {w}"
                else:
                    t.wiki_altnames = w

                t.save()

                # --- Delete original location ---------------------------------
                try:
                    l.delete()
                except Exception as e:
                    print(f"Error deleting id={row['id']}: {e}")
                else:
                    print(f"{row['id']} deleted")
