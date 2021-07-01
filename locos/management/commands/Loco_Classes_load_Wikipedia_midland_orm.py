from csv import DictReader
from django.core.management import BaseCommand

from locos.models import LocoClass

ALREADY_LOADED_ERROR_MESSAGE = """
"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from LocoClass.csv into our LocoClass model"

    def handle(self, *args, **options):
        if LocoClass.objects.exists():
            print('Loco class data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating Loco class")
        for row in DictReader(open('D://MLDatasets/TPAM_DATAIO/Midland_Loco_classes_BSoup.csv')):
            c = LocoClass()
            c.loco_class = row['class']
            c.wheel_arrangement = row['wheel_arrangement']
            c.manufacturer = row['manufacturer'] 
            c.years_built = row['years_built'] 
            c.number_built = row['number_built']
            c.years_withdrawn = row['years_withdrawn'] 
            c.notes = row['notes'] 
            #c.designer = row['designer'] #Load doesn't like this for a foreign key
            c.pre_grouping_company = row['company'] 
            c.grouping_company = row['grouping_company']
            c.save()

