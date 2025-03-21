# Extracts image filenames from a directory and loads records into the mvimages model

from csv import DictReader
from django.core.management import BaseCommand
from mvs.models import HeritageSite
import csv, os
from pathlib import Path

# !!! WARNING - Running this may change the ids of records that are referred to with foreign keys in other tables

#Set up a CSV file and write a Header Row
csv_file = os.path.join("D:\\Data", "TPAM", "mvs_heritagesite.csv")

class Command(BaseCommand):
    def handle(self, *args, **options):
        if HeritageSite.objects.exists():
            print('Military Vehicle Location data already loaded...exiting.')
            return
        print("Creating Military Vehicle Location")
        for row in DictReader(open(csv_file)):
            c = HeritageSite()
            c.id = row['id'] 
            c.site_name = row['site_name']
            c.wikislug = row['wikislug']
            c.url = row['url']
            c.notes = row['notes']
            c.save()
