"""
Extracts the Wikipedia to BRD Mapping currently in TPAM, for further manual updates
"""

from django.core.management import BaseCommand
from locos.models import LocoClass
import os, csv

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):

    def handle(self, *args, **options):

        output_file = os.path.join(DATAIO_DIR, f"Class_BRD_Wikipedia_Mapping.csv")
        with open(output_file, "wt+", newline="", encoding="utf-8") as csvFile:
            output = csv.writer(csvFile)

            csv_output_row = [
                "power_type",
                "wikislug",
                "wikiname",
                "brdslug",
            ]
            output.writerow(csv_output_row)

            lococlasses = LocoClass.objects.all()

            for lococlass in lococlasses:

                csv_output_row = [
                    lococlass.power_type,
                    lococlass.slug,
                    lococlass.name,
                    lococlass.brdslug,
                ]
                output.writerow(csv_output_row)
