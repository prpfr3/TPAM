from csv import DictReader
from django.core.management import BaseCommand
from locations.models import RouteLocation, Location, RouteMap
from django.core.exceptions import ObjectDoesNotExist
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    """

    Imports all RouteLocation records for a given routemap from a CSV file.
    Can be used in conjunction with Route_Locations_Database_Extract.py

    Args:
        routemap_name
    """

    help = """
    Imports all RouteLocation records for a given routemap from a CSV file.

    Example execution statement:
        python manage.py RouteLocations_DB_Extract South_Humberside_Main_Line
    """

    import os

    DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
    os.chdir(DATAIO_DIR)

    def add_arguments(self, parser):
        parser.add_argument(
            "routemap_name",
            type=str,
            help="name of the routemap to import records from",
        )

    def handle(self, *args, **kwargs):

        print("Applying Route Location Manual Changes")

        routemap_name = kwargs["routemap_name"]
        input_file = f"RouteLocations_{routemap_name}.csv"

        with open(os.path.join(DATAIO_DIR, input_file), encoding="utf-8-sig") as file:

            for row in DictReader(file):
                try:

                    rm, rm_created = RouteMap.objects.get_or_create(name=routemap_name)
                except Exception as e:
                    print(f"{rl.loc_no}, {rl.label}, {e}")

                try:
                    rl, rl_created = RouteLocation.objects.get_or_create(
                        loc_no=row["loc_no"],
                        routemap=rm,
                    )

                except Exception as e:
                    print(e)

                rl.loc_no = row["loc_no"]
                if row["label"]:
                    rl.label = row["label"]
                # elif row["name"]:
                #     rl.label = row["name"]
                if row["linear_reference"]:
                    rl.linear_reference = row["linear_reference"]
                rl.note = row["note"]

                if row["location_wikislug"] != "" or None:
                    try:
                        l = Location.objects.get(wikislug=row["location_wikislug"])
                        rl.location_fk = l
                    except ObjectDoesNotExist:
                        missing = row["location_wikislug"]
                        print(
                            f"{rl.loc_no}, {missing} isn't a location wikislug in the Location table"
                        )

                        try:
                            l = Location.objects.get(slug=row["location_wikislug"])
                            rl.location_fk = l
                        except ObjectDoesNotExist:
                            missing = row["location_wikislug"]
                            print(
                                f"{rl.loc_no}, {missing} also isn't a TPAM slug of a location in the Location table"
                            )

                rl.save()

                if rl_created:
                    print(f"New route location created for {row['label']}")
                else:
                    print(f"Existing route location adjusted for {row['label']}")
