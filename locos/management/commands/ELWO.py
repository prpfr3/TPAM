# Extracts Persons from wikipedia saved html page and loads into Oracle

from csv import DictReader
from django.core.management import BaseCommand
from django.db.migrations.operations.fields import RemoveField
from locos.models import Person, PersonRole, Role
import requests, csv, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

#STEP 1: RUN THE SEPARATE WIKI EXTRACT AND DELETE EXTRA ROWS IN EXCEL
#STEP 2: TIDY UP THE CSV FILE FROM WIKIPEDIA WITH PANDAS

DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
filename = os.path.join(DATAIO_DIR, "ETL_Wiki_Persons.csv")

try:
    df = pd.read_csv(filename, header=0, encoding='utf-8')
    df_clean = df.rename(columns={
                       df.columns[0]:"role",
                       df.columns[1]:"wikislug",
                       df.columns[2]:"name"})
    print(df_clean.info())
    print(df_clean.head())
    df_clean.to_csv(os.path.join(DATAIO_DIR, "ETL_Wiki_Persons.csv"), index=False)

except Exception as exc:
    print('Unable to get the file: %s' % (exc))

#STEP 3: THIS PYTHON FILE NEEDS TO BE RUN FROM MANAGE.PY

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from person.csv into our Person model"

    def handle(self, *args, **options):
        if Person.objects.exists():
            print('Person data already loaded...continuing.')
        print("Creating Persons")
        DATAIO_DIR = os.path.join("D:\\MLDatasets", "TPAM_DATAIO")
        filename = os.path.join(DATAIO_DIR, "ETL_Wiki_Persons.csv")  
        count = 0
        for row in DictReader(open(filename)):
            if count == 0:
                count = count + 1
            else:
                print(row)
                role_fk, role_created = Role.objects.get_or_create(
                    role=row['role'],
                    )
                person_fk, role_created = Person.objects.get_or_create(
                    name=row['name'],
                    wikislug = row['wikislug'],
                    url = 'None',
                    notes = 'None'
                    )
                pr = PersonRole()
                pr.role = role_fk
                pr.person = person_fk
                pr.save()
                # c = Person()
                # c.name = row['name'] 
                # c.wikislug = row['wikislug']
                # c.role = role_fk
                # c.url = 'None'
                # c.notes = 'None'
                # c.save()