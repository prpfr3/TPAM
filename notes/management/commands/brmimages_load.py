from csv import DictReader
from django.core.management import BaseCommand
from notes.models import BRMPhotos
import os

DATAIO_DIR = (
    "D:\\OneDrive\\Documents\\Bluebell Railway\\Archive Maps and Plans Database"
)


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads or Updates BRMPhoto metadata from a csv file"

    def handle(self, *args, **options):
        print("Adding Photo Metadata")
        with open(
            os.path.join(DATAIO_DIR, "BRMPhotos.csv"),
            encoding="utf-8-sig",
        ) as file:
            for row in DictReader(file):

                instance = BRMPhotos()

                if row["Reference Number"]:
                    instance.reference_number = row["Reference Number"]
                if row["Key"]:
                    instance.key = row["Key"]
                if row["Company"]:
                    instance.company = row["Company"]
                if row["Class"]:
                    instance.lococlass = row["Class"]
                if row["Date"]:
                    instance.date = row["Date"]
                if row["Number "]:
                    instance.number = row["Number "]
                if row["Name"]:
                    instance.name = row["Name"]
                if row["Location"]:
                    instance.location = row["Location"]
                if row["Train Working"]:
                    instance.train_working = row["Train Working"]
                if row["Other information"]:
                    instance.other_information = row["Other information"]
                if row["Photographer"]:
                    instance.photographer = row["Photographer"]
                if row["Photographer's Ref"]:
                    instance.photographer_ref = row["Photographer's Ref"]
                if row["Sort Date"]:
                    instance.sort_date = row["Sort Date"]
                if row["Day of Week"]:
                    instance.day_of_week = row["Day of Week"]
                if row["Holiday"]:
                    instance.holiday = row["Holiday"]

                try:
                    instance.save()
                    # print(f"{instance} saved")
                except Exception as e:
                    print(f"{instance} not saved due to {e}")
