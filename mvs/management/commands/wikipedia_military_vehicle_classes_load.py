"""
Extracts Military Vehicles from wikipedia saved html page and loads into Oracle
"""

from csv import DictReader
from django.core.management import BaseCommand
from mvs.models import MilitaryVehicleClass
import requests, csv, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

#STEP 1: RUN THE SEPARATE WIKI EXTRACT
#STEP 2: TIDY UP THE CSV FILE FROM WIKIPEDIA WITH PANDAS
#STEP 3: THIS PYTHON FILE NEEDS TO BE RUN FROM MANAGE.PY

class Command(BaseCommand):
    help = "Loads data from ETL_Wiki_List_of_military_vehicles.csv into our Military Vehicle model"

    def handle(self, *args, **options):
        if MilitaryVehicleClass.objects.exists():
            print('Military Vehicle data already loaded...exiting.')
            return
        print("Creating Military Vehicles")
        DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
        filename = os.path.join(DATAIO_DIR, "ETL_Wiki_List_of_military_vehicles.csv")  
        for row in DictReader(open(filename)):
            #print(row.keys())
            c = MilitaryVehicleClass()
            c.mvclass = row['Name'] 
            c.wikislug = row['Slug']
            c.description = row['Description']
            c.notes = 'None'
            c.save()