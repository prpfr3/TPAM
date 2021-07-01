# Extracts Engineers from wikipedia saved html page and loads into Oracle

from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Engineer
import requests, csv, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

#STEP 1: RUN THE SEPARATE WIKI EXTRACT AND DELETE EXTRA ROWS IN EXCEL
#STEP 2: TIDY UP THE CSV FILE FROM WIKIPEDIA WITH PANDAS

DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
filename = os.path.join(DATAIO_DIR, "ETL_Wiki_English_railway_mechanical_engineers.csv")

try:
    df = pd.read_csv(filename, header=0, encoding='utf-8')
    df_clean = df.rename(columns={
                       df.columns[0]:"slug",
                       df.columns[1]:"name"})
    df_clean["slug"].replace('/wiki/', '', regex=True, inplace=True)
    print(df_clean.info())
    print(df_clean.head())
    df_clean.to_csv(os.path.join(DATAIO_DIR, "Engineers.csv"), index=False)

except Exception as exc:
    print('Unable to get the file: %s' % (exc))

#STEP 3: THIS PYTHON FILE NEEDS TO BE RUN FROM MANAGE.PY

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from engineer.csv into our Engineer model"

    def handle(self, *args, **options):
        if Engineer.objects.exists():
            print('Engineer data already loaded...exiting.')
            return
        print("Creating Engineers")
        DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
        filename = os.path.join(DATAIO_DIR, "engineers.csv")  
        for row in DictReader(open(filename)):
            c = Engineer()
            c.eng_name = row['name'] 
            c.wikislug = row['slug']
            c.url = 'None'
            c.notes = 'None'
            c.save()