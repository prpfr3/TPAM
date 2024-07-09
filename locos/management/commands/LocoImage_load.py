"""
Creates a csv file from a directory of photos and loads into the Django image table

To create images in 800x600 select full size images in Windows 10 and then proceed as if sending by email to a user. 
An option will arise which allows the images to be resized.
"""

from csv import DictReader
from django.core.management import BaseCommand
from locations.models import Reference
import csv
import os
from pathlib import Path

# Open the csv input file and write a header record
csv_file = os.path.join("D:\\Data", "TPAM", "RailwayPhotos.csv")

"""
# Beware of overwriting the csv file which has been manually amended 

csvFile = open(csv_file, 'wt+', newline='', encoding='utf-8')
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
    csvrow.append('57863') # To initialise the loco class id
    # Based on the photo name, set the location id then visit id
    if b.startswith('P511'):
      csvrow.append('1209')
      csvrow.append('2')
    elif b.startswith('P511'):
      csvrow.append('1209')
      csvrow.append('2')
    else:
      csvrow.append('1209')
      csvrow.append('2')
    csvrow.append('N/A')
    output.writerow(csvrow)

csvFile.close()
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        # if Image.objects.exists():
        #    print('Railway Heritage images already loaded...exiting.')
        #    return
        print("Creating Railway Heritage Images")
        ref = 10000
        with open(csv_file, encoding="utf-8") as file:
            for row in DictReader(file):
                print(row)
                ref = ref + 1
                c = Reference()
                c.ref = ref
                c.type = 6
                c.full_reference = row['image_name']
                c.image = row['image']
                # c.visit_fk = int(row['visit_fk '])
                c.notes = row['image_name']
                c.save()

                # c = Image()
                # c.image_name = row['image_name']
                # c.image = row['image']
                # c.loco_class_id = int(row['loco_class_id'])
                # c.location_id = int(row['location_id'])
                # c.visit_id = int(row['visit_id'])
                # c.notes = row['notes']
                # c.save()
