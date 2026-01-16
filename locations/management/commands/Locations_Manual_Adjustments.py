from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import Location
from urllib.parse import unquote
import os


class Command(BaseCommand):
    # Show this when the user types help
    help = "Adjusts Locations based on csv input"

    def handle(self, *args, **options):

        print("Making Adjustments")
        DATAIO_DIR = "C:\\Users\\paulf\\OneDrive\\Data\\TPAM"
        with open(
            os.path.join(DATAIO_DIR, "location_updates.csv"), encoding="utf-8-sig"
        ) as file:
            for row in DictReader(file):
                try:
                    l = Location.objects.get(id=row["id"])
                except ObjectDoesNotExist:
                    print(f'No database entry for csv row with id of {row["id"]}')
                except Exception as e:
                    print(f'Error {e} on {row["id"]}')
                else:
                    try:
                        print(f"Before:{l}")
                        if l.wiki_altnames:
                            l.wiki_altnames = f"{l.wiki_altnames}; {row['wikiname']}"
                        else:
                            l.wiki_altnames = row["wikiname"]
                        l.save()
                    except Exception as e:
                        print(f'Error {e} on {row["id"]}')
