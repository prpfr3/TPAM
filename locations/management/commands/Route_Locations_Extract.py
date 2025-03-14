import csv
from django.core.management.base import BaseCommand
from locations.models import RouteLocation


class Command(BaseCommand):
    help = """
    Export all RouteLocation records for a given routemap to a CSV file.

    Example execution statement:
        python manage.py Route_Locations_Extract South_Humberside_Main_Line
    """

    import os

    DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
    os.chdir(DATAIO_DIR)

    def add_arguments(self, parser):
        parser.add_argument(
            "routemap_name",
            type=str,
            help="name of the routemap to extract records for",
        )

    def handle(self, *args, **kwargs):
        routemap_name = kwargs["routemap_name"]
        output_file = f"RouteLocations_DB_Extract_{routemap_name}.csv"

        # Query the records for the given routemap
        records = RouteLocation.objects.filter(routemap__name=routemap_name).order_by(
            "loc_no"
        )

        if not records.exists():
            self.stdout.write(f"No records found for routemap name {routemap_name}")
            return

        # Define the columns for the CSV
        field_names = [
            "id",
            "routemap",
            "loc_no",
            "label",
            "location_fk",
            "location_wikislug",
            "linear_reference",
            "note",
        ]

        # Write to the CSV file
        try:
            with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Write the header
                writer.writerow(field_names)

                # Write the records
                for record in records:
                    writer.writerow(
                        [
                            record.id,
                            record.routemap,
                            record.loc_no,
                            record.label,
                            record.location_fk_id,
                            record.location_fk.wikislug if record.location_fk else None,
                            record.linear_reference,
                            record.note,
                        ]
                    )

            self.stdout.write(
                f"Successfully exported {records.count()} records to {output_file}"
            )

        except Exception as e:
            self.stderr.write(f"An error occurred: {e}")
