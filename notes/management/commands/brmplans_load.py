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
            os.path.join(DATAIO_DIR, "HorshamDrawingBox20 SL Date 2025-02-04.csv"),
            encoding="utf-8-sig",
        ) as file:
            for row in DictReader(file):

                instance = BRMPlans()

                if row["BMARN"]:
                    instance.archivenumber = row["BMARN"]
                if row["LOCATION"]:
                    instance.location = row["LOCATION"]
                if row["DESCRIPTION"]:
                    instance.description = row["DESCRIPTION"]
                if row["SCALE"]:
                    instance.number = row["SCALE"]
                if row["Copies/Sheets"]:
                    instance.date = row["Copies/Sheets"]
                if row["ORIGIN"]:
                    instance.date = row["ORIGIN"]
                if row["DATE"]:
                    instance.date = row["DATE"]
                if row["TUBE No"]:
                    instance.tube = row["TUBE No"]
                if row["Roll"]:
                    instance.roll = row["Roll"]
                if row["Drawing No. "]:
                    instance.drawingno = row["Drawing No. "]
                if row["Negative No."]:
                    instance.negativeno = row["Negative No."]
                if row["Material"]:
                    instance.material = row["Material"]
                if row["ThumbnailPhotoId"]:
                    instance.material = row["ThumbnailPhotoId"]

                try:
                    instance.save()
                    # print(f"{instance} saved")
                except Exception as e:
                    print(f"{instance} not saved due to {e}")
