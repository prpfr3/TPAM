from csv import DictReader
from django.core.management import BaseCommand

from locos.models import ModernClass

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first truncate the sql table to remove existing values."""

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv into the ModernClass model"

    def handle(self, *args, **options):
        if ModernClass.objects.exists():
            print('Class data already loaded...exiting.')
            print(ALREADY_LOADED_ERROR_MESSAGE)
            return
        print("Creating classes")
        import os
        for csv in [
            'Class_BRD_Diesel.csv',
            'Class_BRD_Electric.csv'
          ]:

          with open(os.path.join("D:\\Data", "TPAM", csv), encoding="utf-8") as file:   
              for row in DictReader(file):

                c = ModernClass()
                c.class_type = row['Class Type'] 
                c.modern_class = row['Class']
                c.modern_class_slug = row['Class_url']
                c.year_introduced = row['Introduced']
                c.manufacturer = row['Manufacturer'] 
                if c.class_type == 'D':
                  c.power_unit = row['Power Unit']
                  c.horse_power = row['Horse Power']
                  c.transmission = row['Transmission'] 
                elif c.class_type == 'E':
                  c.current = row['Current']
                  c.aka_class = row['AKA']
                  c.aka_class_slug = row['AKA_url']
                c.wheel_id = row['Wheels']
                c.wheel_id_slug = row['Wheels_url']
                c.number_range = row['Number Range']
                c.number_range_slug = row['Number Range_url']
                c.number_built = row['Number']
                c.multiple = row['Multiple']
                c.img_slug = row['Thumbnail_img']
                c.save()