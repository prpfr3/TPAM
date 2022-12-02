# Takes engineers extracted from various category pages of wikipedia along with a list extracted from Grace's Guide 
# and loads the engineers into the database along with a reference slug to Grace's guide.

import os
import pandas as pd

from csv import DictReader
from django.core.management import BaseCommand
from locos.models import Person, PersonRole, Role

#STEP 1: RUN THE SEPARATE EXTRACTS FOR GRACE AND WIKIPEDIA AND DELETE EXTRA ROWS IN EXCEL IF NECESSARY
#STEP 2: TIDY UP THE CSV FILE FROM WIKIPEDIA WITH PANDAS

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
wiki_filename = os.path.join(DATAIO_DIR, "Persons_Extract_Wikipedia.csv")

df_wiki = pd.read_csv(wiki_filename, header=0, encoding='utf-8')
df_wiki_clean = df_wiki.rename(columns={
                    df_wiki.columns[0]:"role",
                    df_wiki.columns[1]:"wikitextslug",
                    df_wiki.columns[2]:"name",
                    df_wiki.columns[3]:"firstnames",
                    df_wiki.columns[4]:"surname",
                    })
df_wiki_clean.set_index("name", inplace=True)
print(df_wiki_clean.info())
print(df_wiki_clean.head())

grace_filename = os.path.join(DATAIO_DIR, "Persons_Extract_Grace.csv")

df_grace = pd.read_csv(grace_filename, header=0, encoding='utf-8')
df_grace_clean = df_grace.rename(columns={
                    df_grace.columns[0]:"gracetextslug",
                    df_grace.columns[1]:"name",
                    df_grace.columns[2]:"firstnames",
                    df_grace.columns[3]:"surname",
                    })
df_grace_clean.set_index("name", inplace=True)
print(df_grace_clean.info())
print(df_grace_clean.head())

df_merged = df_wiki_clean.join(df_grace_clean, rsuffix='grace_')
df_merged.reset_index(inplace=True)
df_merged.to_csv(os.path.join(DATAIO_DIR, "Persons_Load.csv"), index=False)

#STEP 3: Load the engineers into the database
class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from person.csv into our Person model"

    def handle(self, *args, **options):
        if Person.objects.exists():
            print('Engineers already loaded...but continuing.')
        else:
            print("Loading Engineers for the first time")
        count = 0

        #This form of statement top ensure correct treatement of unusual unicode characters
        with open(os.path.join("D:\\Data", "TPAM", "Persons_Load.csv"), encoding="utf-8") as file:   

            for row in DictReader(file):
                if count == 0:
                    count = count + 1
                else:
                    print(row)
                    role_fk, role_created = Role.objects.get_or_create(
                        role=row['role'],
                        )
                    # Exclude these names that are wrong assigned from Grace's guide to Wikipedia equivalents    
                    if row['gracetextslug'] not in [
                        "/Henry_Fowler_(1821-1854)",
                        "/James_Johnson_(2)",
                        "/John_Grantham_(2)"]:
                        person_fk, person_created = Person.objects.get_or_create(
                            name=row['name'],
                            firstname=row['firstnames'],
                            surname=row['surname'],
                            wikitextslug = row['wikitextslug'].replace("/wiki/",""),
                            gracetextslug = row['gracetextslug'].replace("/",""),
                            notes = 'None'
                            )
                        pr = PersonRole()
                        pr.role = role_fk
                        pr.person = person_fk
                        pr.save()