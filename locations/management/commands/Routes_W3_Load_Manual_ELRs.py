from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Route, ELR
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    help = "Load of ELRs for a route from a manually maintained csv file"

    def handle(self, *args, **options):

        with open(os.path.join(DATAIO_DIR, "Routes_ELRs_Manual_Mapping.csv"), encoding="utf-8-sig") as file:

            for row in DictReader(file):
                # Check the route exists and get the key

                try:
                    route_fk = Route.objects.get(
                        wikipedia_slug=row['route_wikislug'])
                    print(f'{route_fk} found')
                except ObjectDoesNotExist:
                    print(f"{row['route_wikislug']} is not in the Routes table")
                except MultipleObjectsReturned:
                    print(
                        f"{row['route_wikislug']} has multiple entries in the Routes table")
                else:

                    # Check the elr exists and get the key
                    try:
                        elr_fk = ELR.objects.get(itemAltLabel=row['elr'])
                        print(f'{elr_fk} found')
                    except ObjectDoesNotExist:
                        print(f"{row['elr']} is not in the ELR table")
                    except MultipleObjectsReturned:
                        print(
                            f"{row['elr']} has multiple entries in the ELR table")

                    # Add the route to the ELR (This does not seem to add duplicates where the record already exists)
                    else:
                        route_fk.elrs.add(elr_fk)
