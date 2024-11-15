"""
Extracts geojson data from the ELRs table into a CSV file
"""

from django.core.management import BaseCommand
import os
import csv
from locations.models import ELR

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    def handle(self, *args, **options):
        # File path for the output CSV
        output_file = os.path.join(DATAIO_DIR, "ELR_geojsons.csv")

        # Query the ELR model for id and geojson fields
        queryset = ELR.objects.only("id", "geojson")

        # Write to CSV
        with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
            # Define the CSV writer and headers
            writer = csv.writer(csvfile, delimiter="|")
            writer.writerow(["id", "geojson"])  # CSV header

            for instance in queryset:
                # Write each instance's fields to the CSV
                writer.writerow([instance.id, instance.geojson])

        self.stdout.write(f"Data exported to {output_file}")
