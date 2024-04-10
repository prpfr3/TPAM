from csv import DictReader
from django.core.management import BaseCommand
from notes.models import BRMPlans
import os

DATAIO_DIR = (
    "D:\\OneDrive\\Documents\\Bluebell Railway\\Archive Maps and Plans Database"
)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads or Updates BRM Plans and Maps from a csv file"

    def handle(self, *args, **options):
        print("Adding Plans and Map")
        with open(
            os.path.join(DATAIO_DIR, "HorshamDrawingBox20 SL Date 2024-01-10 PF.csv"),
            encoding="utf-8-sig",
        ) as file:
            for row in DictReader(file):

                instance = BRMPlans()

                if row["archivenumber"]:
                    instance.archivenumber = row["archivenumber"]
                if row["location"]:
                    instance.location = row["location"]
                if row["description"]:
                    instance.description = row["description"]
                if row["scale"]:
                    instance.scale = row["scale"]
                if row["number"]:
                    instance.number = row["number"]
                if row["origin"]:
                    instance.origin = row["origin"]
                if row["date"]:
                    instance.date = row["date"]
                if row["tube"]:
                    instance.tube = row["tube"]
                if row["roll"]:
                    instance.roll = row["roll"]
                if row["drawingno"]:
                    instance.drawingno = row["drawingno"]
                if row["negativeno"]:
                    instance.negativeno = row["negativeno"]
                if row["material"]:
                    instance.material = row["material"]

                try:
                    instance.save()
                    # print(f"{instance} saved")
                except Exception as e:
                    print(f"{instance} not saved due to {e}")
