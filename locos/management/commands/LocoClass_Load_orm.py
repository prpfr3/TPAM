from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import LocoClass, WheelArrangement

ALREADY_LOADED_ERROR_MESSAGE = "To reload the data from the CSV file,first either (a) delete and recreate the database table to reset keys to start at zero or (b) drop all the table records in which cases the keys will be initialised starting at the last unused value"

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
        DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
        for csv in [
          'Master_List_of_Steam_Classes.csv',
          ]:
          for row in DictReader(open(os.path.join(DATAIO_DIR, csv), encoding='utf-8')):
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

              """
              #Prints are to provide a trace if any datafield is too long
              print(c.grouping_company, len(row['Big 4']))
              print(c.pre_grouping_company, len(row['Pre Grouping']))
              print(c.designer, len(row['\ufeffDesigner']))
              print(c.designer_slug, len(row['Designer_url']))
              print(c.grouping_class, len(row['Class']))
              print(c.grouping_class_slug, len(row['Class_url']))
              print(c.pre_grouping_class, len(row['Pre Grouping Class'])) 
              print(c.br_power_class, len(row['BR Power Class']))
              print(c.wheel_id, len(row['Wheels']))
              print(c.whyte_notation_id, len(row['Wheel_url']))
              print(c.year_built, len(row['Year']))
              print(c.number_range, len(row['Number Range'])) 
              print(c.number_range_slug, len(row['Number Range_url'])) 
              print(c.year_first_built, len(row['First']))
              print(c.year_last_built, len(row['Last']))
              print(c.number_built, len(row['#']))
              print(c.img_slug, len(row['Thumbnail_img']))
              """
              c.save()