# Extracts image filenames from a directory and loads records into the images model

from csv import DictReader
from django.core.management import BaseCommand
from aircraft.models import AirImage
import csv, os
from pathlib import Path

# !!! WARNING - Running this may change the ids of records that are referred to with foreign keys in other tables

#Set up a CSV file and write a Header Row
csv_file = os.path.join("D:\\Data", "TPAM", "ETL_Wiki_AircraftImages.csv")
csvFile = open(csv_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
output.writerow(['image_name', 'image', 'aircraft_class_id', 'location_id', 'visit_id', 'notes'])

##Get the filenames of all the image files
allfiles = Path(os.path.join("D:\\Pictures\ZZAircraft\ZZAircraft800x600")).glob('**/*.jpg')
flist = sorted(allfiles)

for f in flist:
    csvrow = []
    b = os.path.basename(f)
    csvrow.append(b)
    csvrow.append(b)
    csvrow.append('1')
    #location id then visit id
    if b.startswith('P511'):
      csvrow.append('1')
      csvrow.append('1')
    elif b.startswith('P511'):
      csvrow.append('1')
      csvrow.append('1')
    else:
      csvrow.append('1')
      csvrow.append('1')
    csvrow.append('N/A')
    output.writerow(csvrow)

csvFile.close()

class Command(BaseCommand):
    def handle(self, *args, **options):
        if AirImage.objects.exists():
            print('Aircraft images already loaded...exiting.')
            return
        print("Creating Aircraft Images")
        for row in DictReader(open(csv_file)):
            c = AirImage()
            c.image_name = row['image_name'] 
            c.image = row['image']
            c.airclass_id = int(row['aircraft_class_id'])
            c.location_id = int(row['location_id'])
            c.visit_id = int(row['visit_id'])
            c.notes = row['notes']
            c.save()