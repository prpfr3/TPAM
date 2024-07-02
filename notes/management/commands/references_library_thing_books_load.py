from csv import DictReader
from django.core.management import BaseCommand
from notes.models import Reference
import os

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads or Updates References from a csv file"

    def handle(self, *args, **options):
        print("Adding References")
        with open(
            os.path.join("D:\\OneDrive\\My Books", "librarything_prpfr3_railway.csv"),
            encoding="utf-8-sig",
        ) as file:
            for row in DictReader(file):

                try:
                    r_fk, reference_created = Reference.objects.get_or_create(
                        ltbookid=row["Book ID"], type=1
                    )
                except Exception as e:
                    print(e)

                r_fk.type = 1
                r_fk.ltbookid = row["Book ID"]
                if row["ISBN"]:
                    r_fk.isbn = "".join(
                        filter(str.isdigit, row["ISBN"])
                    )  # Strips out non numbers
                if row["Title"]:
                    r_fk.title = row["Title"]
                if row["Date"]:
                    r_fk.year = row["Date"]
                if row["Primary Author"]:
                    r_fk.authors = row["Primary Author"]

                try:
                    r_fk.save()
                    print(f"{r_fk} saved")
                except Exception as e:
                    print(f"{r_fk} not saved due to {e}")
