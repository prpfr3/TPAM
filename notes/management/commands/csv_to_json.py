import csv
import json
import os

from django.core.management import BaseCommand


class Command(BaseCommand):

  def handle(self, *args, **options):

    DATAIO_DIR = (
        "C:\\users\\paulf\\OneDrive\\Documents\\Bluebell Railway\\Archive Maps and Plans Database"
    )

    with open(os.path.join(DATAIO_DIR, "Maps_and_Plans.csv"), newline='', encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)

    with open(os.path.join(DATAIO_DIR, "Maps_and_Plans.json"), "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=2)
