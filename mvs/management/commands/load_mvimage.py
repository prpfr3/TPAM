# Extracts image filenames from a directory and loads records into the mvimages model

from csv import DictReader
from django.core.management import BaseCommand
from mvs.models import MVImage
import csv, os
from pathlib import Path

# !!! WARNING - Running this may change the ids of records that are referred to with foreign keys in other tables

#Set up a CSV file and write a Header Row
csv_file = os.path.join("D:\\Data", "TPAM", "ETL_Wiki_MVImages.csv")
#csvFile = open(csv_file, 'wt+', newline='', encoding='utf-8')
#output = csv.writer(csvFile)
#output.writerow(['image_name', 'image', 'mvclass_id', 'location_id', 'visit_id', 'notes'])

##Get the filenames of all the image files
#allfiles = Path(os.path.join("D:\\Pictures\ZZMilitaryVehicles\ZZMilitaryVehicles800x600")).glob('**/*.jpg')
#flist = sorted(allfiles)

#for f in flist:
#    csvrow = []
#    b = os.path.basename(f)
#    csvrow.append(b)
#    csvrow.append(b)
#    csvrow.append('1')
#    #location id then visit id
#    if b.startswith('Bovingdon'):
#      csvrow.append('1')
#      csvrow.append('7')
#    elif b.startswith('Duxford'):
#      csvrow.append('3')
#      csvrow.append('8')
#    elif b.startswith('P511'):
#      csvrow.append('4')
#      csvrow.append('9')
#    elif b.startswith('P807'):
#      csvrow.append('2')
#      csvrow.append('6')
#    elif b.startswith('P818'):
#      csvrow.append('1')
#      csvrow.append('5')
#    elif b.startswith('PA161'):
#      csvrow.append('6')
#      csvrow.append('11')
#    elif b.startswith('PA221'):
#      csvrow.append('6')
#      csvrow.append('11')
#    elif b.startswith('PC31'):
#      csvrow.append('5')
#      csvrow.append('10')
#    else:
#      csvrow.append('1')
#      csvrow.append('1')
#    csvrow.append('Enter Notes here:')
#    output.writerow(csvrow)

#csvFile.close()

class Command(BaseCommand):
    def handle(self, *args, **options):
        if MVImage.objects.exists():
            print('Military Vehicle images already loaded...exiting.')
            return
        print("Creating Military Vehicle Images")
        for row in DictReader(open(csv_file)):
            c = MVImage()
            c.image_name = row['image_name'] 
            c.image = row['image']
            c.mvclass_id = int(row['mvclass_id'])
            c.location_id = int(row['location_id'])
            c.visit_id = int(row['visit_id'])
            c.notes = row['notes']
            c.save()