import os
import pandas as pd
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from companies.models import ClassDesigner, Company, Manufacturer
from people.models import Person
from locos.models import LocoClass

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
TEMP_FILE = 'Class_W5_Load_Designers_Temp.csv'
output_file = os.path.join(DATAIO_DIR, TEMP_FILE)

cleaned = os.path.join(DATAIO_DIR, 'Class_All_W3_Cleansed_Detail.csv')
df_cleaned = pd.read_csv(cleaned, header=0, encoding='utf-8')
df_cleaned_designers = df_cleaned.loc[df_cleaned['2'] == 'Designer']
# print(df_cleaned_designers.head())
df_cleaned_designers.drop(df_cleaned_designers.columns.difference(['0','3', '4', '5', '6', '7']), 1, inplace=True) # Drops the columns beyond 8
df_cleaned_designers.drop_duplicates(subset=['0','3', '4', '5', '6', '7'], inplace=True) # Theoretically redundant if duplicates dropped when cleansing detail
# print(df_cleaned_designers.head())
df_cleaned_designers.to_csv(output_file, index=False, encoding='utf-8')

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the ClassManufacturer model"

    def handle(self, *args, **options):
        if ClassDesigner.objects.exists():
            print('Some LocoClass Designer entries already loaded but continuing with this load...')

        with open(os.path.join(DATAIO_DIR, TEMP_FILE), encoding="utf-8") as file:   
            for row in DictReader(file):
                c = ClassDesigner()
                try:
                    slug = row['0'].replace('/wiki/', '')
                    c.lococlass_fk = LocoClass.objects.get(lococlasslist__wikislug=slug)
                except ObjectDoesNotExist:
                    print(f'{slug} not found in the Lococlass wikipedia_slug field')
                else:
                    columns = ['4', '5', '6', '7']

                    for column in columns:  
                        if row[column] != "":
                            try:
                                slug = row[column].replace('/wiki/','')
                                c.manufacturer_fk = Manufacturer.objects.get(wikislug=slug)
                                c.save()
                            except ObjectDoesNotExist:
                                try:
                                    c.person_fk = Person.objects.get(wikitextslug=slug)
                                    c.save()
                                except ObjectDoesNotExist:
                                    try:
                                        c.company_fk = Company.objects.get(wikislug=slug)
                                        c.save()
                                    except Exception:
                                        print(slug, ' not in the company, person or manufacturer table')
                                        continue