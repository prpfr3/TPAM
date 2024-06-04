import csv, os
from django.core.management.base import BaseCommand
from locations.models import LocationEvent


class Command(BaseCommand):
    help = "Export LocationEvent data to a CSV file"

    def handle(self, *args, **kwargs):
        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        file_path = os.path.join(DATAIO_DIR, "location_events.csv")
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write CSV header
            writer.writerow(
                [
                    "Type",
                    "Type Description",
                    "Description",
                    "Date",
                    "Datefield",
                    "Route ID",
                    "Route Name",
                    "Company ID",
                    "Company Name",
                    "Location ID",
                    "Location Name",
                    "ELR ID",
                    "ELR Name",
                    "Post ID",
                    "Post Name",
                    "Date Added",
                ]
            )

            # Fetch and write data rows
            for event in LocationEvent.objects.all():
                writer.writerow(
                    [
                        event.type,
                        event.get_type_display(),
                        event.description,
                        event.date,
                        event.datefield,
                        event.route_fk.id if event.route_fk else "",
                        event.route_fk.wikipedia_slug if event.route_fk else "",
                        event.company_fk.id if event.company_fk else "",
                        event.company_fk.wikislug if event.company_fk else "",
                        event.location_fk.id if event.location_fk else "",
                        event.location_fk.name if event.location_fk else "",
                        event.elr_fk.id if event.elr_fk else "",
                        event.elr_fk.slug if event.elr_fk else "",
                        # event.post_fk.id if event.post_fk else "",
                        # event.post_fk.name if event.post_fk else "",
                        event.date_added,
                    ]
                )

        self.stdout.write(
            self.style.SUCCESS(f"Data successfully exported to {file_path}")
        )
