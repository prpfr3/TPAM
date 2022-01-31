"""
Extracts photo image records from a CSV file and loads records into the images model

If you have previously loaded images and referred to their image ids through foreign keys then be careful not to change or erase the image ids of the images already loaded.
"""

from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Image
import csv, os
from pathlib import Path

#Open the csv input file and write a header record
input_file = os.path.join("D:\\Data", "TPAM", "RailwayPhotos.csv")
csvFile = open(input_file, 'wt+', newline='', encoding='utf-8')
output = csv.writer(csvFile)
output.writerow(['image_name', 'image', 'loco_class_id', 'location_id', 'visit_id', 'notes'])

##Get the filenames of all the image files
allfiles = Path(os.path.join("D:\\Pictures\ZZRailwayHeritage\ZZRailwayHeritage800x600")).glob('**/*.jpg')
flist = sorted(allfiles)

for f in flist:
    csvrow = []
    b = os.path.basename(f)
    csvrow.append(b) # To be used as the image name
    csvrow.append(b) # To be used as a reference to the actual image file
    csvrow.append('1') # To initialise the loco class id
    # Based on the photo name, set the location id then visit id
    if b.startswith('P511'):
      csvrow.append('48')
      csvrow.append('3')
    elif b.startswith('P511'):
      csvrow.append('48')
      csvrow.append('3')
    else:
      csvrow.append('48')
      csvrow.append('3')
    csvrow.append('N/A')
    output.writerow(csvrow)

csvFile.close()

class Command(BaseCommand):
    def handle(self, *args, **options):
        #if Image.objects.exists():
        #    print('Railway Heritage images already loaded...exiting.')
        #    return
        print("Creating Railway Heritage Images")
        for row in DictReader(open(csv_file)):
            print(row)
            c = Image()
            c.image_name = row['image_name'] 
            c.image = row['image']
            c.loco_class_id = int(row['loco_class_id'])
            c.location_id = int(row['location_id'])
            c.visit_id = int(row['visit_id'])
            c.notes = row['notes']
            c.save()