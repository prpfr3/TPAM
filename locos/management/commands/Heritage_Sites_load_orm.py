from csv import DictReader
from django.core.management import BaseCommand

from locos.models import HeritageSite

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from ETL_Wiki_List_of_British_heritage_and_private_railways.csv into the HeritageSite model. Note that this csv has been prepared manually based on Wikipedia data and cannot be easily reextracted from Wikipedia (due to the difficulties of separating and denoting standard and narrow gauge railways"

    def handle(self, *args, **options):
        if HeritageSite.objects.exists():
            print('Heritage Sites already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating Heritage Sites")
        import os
        for csv in [
          'ETL_Wiki_List_of_British_heritage_and_private_railways.csv'
          ]:
            with open(os.path.join("D:\\Data", "TPAM", csv), encoding="utf-8") as file:   
                for row in DictReader(file):
                    c = HeritageSite()
                    c.site_name = row['location'] 
                    c.wikislug = row['url']
                    c.save()
