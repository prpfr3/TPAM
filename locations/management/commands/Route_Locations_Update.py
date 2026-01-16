from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locations.models import RouteLocation
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
                if row["replaced_by"]:
                    try:
                        queryset = RouteLocation.objects.filter(id=row["replaced_by"])
                    except Exception as e:
                        print(f'Error {e} on {row["id"]}')
                    else:
                        print(f'{queryset=} for {row["id"]}')
                        for record in queryset:
                            try:
                                print(f"Before:{record.location_fk} After:{row['id']}")
                                record.location_fk = row["id"]
                                # record.save()
                            except Exception as e:
                                print(f'Error {e} on {row["id"]}')
