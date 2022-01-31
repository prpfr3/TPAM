# Extracts image filenames from a directory and loads records into the mvimages model

from csv import DictReader
from django.core.management import BaseCommand
from mvs.models import Visit
import csv, os
from pathlib import Path

# !!! WARNING - Running this may change the ids of records that are referred to with foreign keys in other tables

#Set up a CSV file and write a Header Row
csv_file = os.path.join("D:\\Data", "TPAM", "mvs_visit.csv")

class Command(BaseCommand):
    def handle(self, *args, **options):
        if Visit.objects.exists():
            print('Military Vehicle Visits data already loaded...exiting.')
            return
        print("Creating Visits")
        for row in DictReader(open(csv_file)):
            c = Visit()
            c.id = row['id'] 
            c.date = row['date']
            c.notes = row['notes']
            c.location_id = row['location_id']
            c.save()

