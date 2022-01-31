from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass, WheelArrangement

ALREADY_LOADED_ERROR_MESSAGE = "To reload the data from the CSV file,first either \
drop all the table records in which cases the keys will be initialised starting at \
  the last unused value"

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into a LocoClass model"

    def handle(self, *args, **options):
        #if LocoClass.objects.exists():
        #    print('LocoClass data already loaded...exiting.')
        #    print(ALREADY_LOADED_ERROR_MESSAGE)
        #    return
        print("Creating Loco class")
        import os
        DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
        for csv in [
          'Master_List_of_Steam_Classes.csv',
          ]:

          with open(os.path.join(DATAIO_DIR, csv), encoding="utf-8") as file:   
              for row in DictReader(file):

                  c = LocoClass()
                  #print(row)
                  c.grouping_company = row['Big 4']
                  c.pre_grouping_company = row['Pre Grouping']
                  c.designer = row['\ufeffDesigner'] #A fudge to remove the https://en.wikipedia.org/wiki/Byte_order_markcharacter put there by Windows which interferes with utf-8 coding
                  c.designer_slug = row['Designer_url']
                  c.grouping_class = row['Class']
                  c.grouping_class_slug = row['Class_url']
                  c.pre_grouping_class = row['Pre Grouping Class'] 
                  c.br_power_class = row['BR Power Class']
                  c.wheel_body_type = row['Wheels']
                  try:
                    c.wheel_arrangement = WheelArrangement.objects.get(whyte_notation=row['Wheel_url'])
                  except ObjectDoesNotExist:
                      print('No wheel notation lookup entry for ', c.wheel_arrangement, ' ', row['Wheel_url'])
                  c.year_built = row['Year']
                  c.number_range = row['Number Range'] 
                  c.number_range_slug = row['Number Range_url'] 
                  c.year_first_built = row['First']
                  c.year_last_built = row['Last']
                  c.number_built = row['#']
                  c.img_slug = row['Thumbnail_img']
                  c.save()