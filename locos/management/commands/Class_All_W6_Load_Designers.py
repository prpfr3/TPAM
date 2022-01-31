import os
import pandas as pd
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from locos.models import ClassDesigner, Company, Builder, Person, LocoClass

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
TEMP_FILE = 'Class_W6_Load_Designers_Temp.csv'
output_file = os.path.join(DATAIO_DIR, TEMP_FILE)
load_type = "STEAM"

if load_type == "MODERN":
    cleaned = os.path.join(DATAIO_DIR, 'Class_Modern_W3_Cleansed_Detail.csv')
    df_cleaned = pd.read_csv(cleaned, header=0, encoding='utf-8')
    df_cleaned_designers = df_cleaned.loc[df_cleaned['2'] == 'Designer']
    df_cleaned_designers.drop(df_cleaned_designers.columns.difference(['0', '3', '4', '5', '6', '7']), 1, inplace=True)
    df_cleaned_designers.to_csv(output_file, index=False, encoding='utf-8')
elif load_type == "STEAM":
    designers = os.path.join(DATAIO_DIR, 'Class_Steam_Manually_Cleansed_Designer_to_Designer_Slug.csv')
    cleaned = os.path.join(DATAIO_DIR, 'Class_Steam_W3_Detail_Cleansed.csv')
    df_designers = pd.read_csv(designers, header=0, encoding='utf-8')
    df_cleaned = pd.read_csv(cleaned, header=0, encoding='utf-8')
    df_cleaned_designers = df_cleaned.loc[df_cleaned['2'] == 'Designer']
    df_cleaned_designers.drop(df_cleaned_designers.columns.difference(['0', '3']), 1, inplace=True)
    df_merged_designers = df_cleaned_designers.merge(df_designers, left_on=['3'], right_on=['Column4'], how='left')
    df_merged_designers.drop(['3', 'Column4'], axis=1, inplace=True)
    df_merged_designers.to_csv(output_file, index=False, encoding='utf-8')

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the ClassBuilder model"

    def handle(self, *args, **options):
        if ClassDesigner.objects.exists():
            print('Some LocoClass Designer entries already loaded but continuing with this load...')
            pass

        with open(os.path.join(DATAIO_DIR, TEMP_FILE), encoding="utf-8") as file:   
            for row in DictReader(file):

                c = ClassDesigner()
                try:
                    c.lococlass_fk = LocoClass.objects.get(grouping_class_slug=row['0'])
                except ObjectDoesNotExist:
                    print(row['0'], ' not found in the Lococlass grouping_class_slug field')

                if load_type == "MODERN":
                    columns = ['4', '5', '6', '7']
                elif load_type == "STEAM":
                    columns = ['Column5', 'Column6', 'Column7']
                else:
                    print("Invalid Load Type: Neither Steam nor diesel")
                    break
                for column in columns:

                    if row[column] != "":
                        print('\nDesigner', row[column], ':-')
                        try:
                            c.person_fk = Person.objects.get(wikitextslug=row[column])
                            c.save()
                            print(' is a person and has been recorded as the designer')
                        except:
                            print(' is not a person')

                            try:
                                c.company_fk = Company.objects.get(wikislug=row[column])
                                c.save()
                                print(' is a company and has been recorded as the designer')
                            except:
                                print(' is not a company')

                                try:
                                    c.builder_fk = Builder.objects.get(wikislug=row[column])
                                    c.save()
                                    print(' is a manufacturer and has been recorded as the designer')
                                except ObjectDoesNotExist:
                                    print(' is not a manufacturer')
                                    pass
                                except MultipleObjectsReturned:
                                    print(row[column], ' is in the manufacturer table more than once')
                                    pass