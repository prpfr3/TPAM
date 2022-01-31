import os
import pandas as pd
from csv import DictReader
from django.core.management import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from locos.models import ClassBuilder, Company, Builder, Person, LocoClass

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
TEMP_FILE = 'Class_W5_Load_Builders_Temp.csv'
output_file = os.path.join(DATAIO_DIR, TEMP_FILE)
load_type = "MODERN"

if load_type == "MODERN":
    cleaned = os.path.join(DATAIO_DIR, 'Class_Modern_W3_Cleansed_Detail.csv')
    df_cleaned = pd.read_csv(cleaned, header=0, encoding='utf-8')
    df_cleaned_builders = df_cleaned.loc[df_cleaned['2'] == 'Builder']
    df_cleaned_builders.drop(df_cleaned_builders.columns.difference(['0', '3', '4', '5', '6', '7']), 1, inplace=True)
    df_cleaned_builders.to_csv(output_file, index=False, encoding='utf-8')
elif load_type == "STEAM":
    builders = os.path.join(DATAIO_DIR, 'Class_Steam_Manually_Cleansed_Builder_to_Builder_Slug.csv')
    cleaned = os.path.join(DATAIO_DIR, 'Class_Steam_W3_Detail_Cleansed.csv')
    df_builders = pd.read_csv(builders, header=0, encoding='utf-8')
    df_cleaned = pd.read_csv(cleaned, header=0, encoding='utf-8')
    df_cleaned_builders = df_cleaned.loc[df_cleaned['2'] == 'Builder']
    df_cleaned_builders.drop(df_cleaned_builders.columns.difference(['0', '3']), 1, inplace=True)
    df_merged_builders = df_cleaned_builders.merge(df_builders, left_on=['3'], right_on=['a'], how='left')
    df_merged_builders.drop(['3', 'a'], axis=1, inplace=True)
    df_merged_builders.to_csv(output_file, index=False, encoding='utf-8')

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from a csv file into the ClassBuilder model"

    def handle(self, *args, **options):
        if ClassBuilder.objects.exists():
            print('Some LocoClass Builder entries already loaded but continuing with this load...')
            pass

        with open(os.path.join(DATAIO_DIR, TEMP_FILE), encoding="utf-8") as file:   
            for row in DictReader(file):

                c = ClassBuilder()
                try:
                    c.lococlass_fk = LocoClass.objects.get(grouping_class_slug=row['0'])
                except ObjectDoesNotExist:
                    print(row['0'], ' not found in the Lococlass grouping_class_slug field')
                
                if load_type == "MODERN":
                    columns = ['4', '5', '6', '7']
                elif load_type == "STEAM":
                    columns = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
                else:
                    print("Invalid Load Type: Neither Steam nor diesel")
                    break
                for column in columns:
                    if row[column] == "/wiki/Ashford_railway_works": row[column] = "/wiki/Ashford_railway_works"
                    if row[column] == "/wiki/Ashford_Works": row[column] = "/wiki/Ashford_railway_works"
                    if row[column] == "/wiki/Vulcan_Iron_Works": row[column] = "/wiki/Vulcan_Iron_Works#Locomotives"
                    if row[column] == "/wiki/H._K._Porter,_Inc": row[column] = "/wiki/H.K._Porter,_Inc."
                    if row[column] == "/wiki/Hawthorn_Leslie_and_Company": row[column] = "/wiki/R._%26_W._Hawthorn,_Leslie_and_Company"
                    if row[column] == "/wiki/Hawthorn_Leslie": row[column] = "/wiki/R._%26_W._Hawthorn,_Leslie_and_Company"
                    if row[column] == "/wiki/Nasmyth,_Gaskell_and_Company": row[column] = "/wiki/Nasmyth,_Gaskell_and_Company"
                    if row[column] == "/wiki/Vulcan_Foundry": row[column] = "/wiki/Vulcan_Foundry"
                    if row[column] == "/wiki/Neilson_and_Company": row[column] = "/wiki/Neilson_and_Company"
                    if row[column] == "/wiki/Kerr,_Stuart_and_Company ": row[column] = "/wiki/Kerr,_Stuart_and_Company"
                    if row[column] == "/wiki/St._Rollox_railway_works": row[column] = "/wiki/Glasgow_Works"
                    if row[column] == "/wiki/Sharp,_Stewart_and_Company": row[column] = "/wiki/Sharp,_Stewart_and_Company"
                    if row[column] == "/wiki/Gorton_locomotive_works": row[column] = "/wiki/Gorton_Locomotive_Works"
                    if row[column] == "/wiki/Gorton_Works": row[column] = "/wiki/Gorton_Locomotive_Works"
                    if row[column] == "/wiki/North_British_Locomotive_Co.": row[column] = "/wiki/North_British_Locomotive_Company"
                    if row[column] == "/wiki/Beyer,_Peacock_%26_Co.": row[column] = "/wiki/Beyer,_Peacock_and_Company"
                    if row[column] == "/wiki/Kitson_%26_Co.": row[column] = "/wiki/Kitson_and_Company"
                    if row[column] == "/wiki/Yorkshire_Engine_Co.": row[column] = "/wiki/Yorkshire_Engine_Company"
                    if row[column] == "/wiki/Electro-Motive_Diesel": row[column] = "/wiki/Yorkshire_Engine_Company"
                    if row[column] == "/wiki/F._C._Hibberd_%26_Co_Ltd": row[column] = "/wiki/F._C._Hibberd_%26_Co."
                    if row[column] == "/wiki/Harland_%26_Wolff": row[column] = "/wiki/Harland_and_Wolff"
                    if row[column] == "/wiki/Ruston_%26_Hornsby": row[column] = "/wiki/Ruston_(engine_builder)#Ruston_&_Hornsby"
                    if row[column] == "/wiki/Vossloh_Espa%C3%B1a": row[column] = "/wiki/MACOSA#Vossloh_Espa%C3%B1a"                
                    if row[column] != "":
                        try:
                            c.builder_fk = Builder.objects.get(wikislug=row[column])
                            c.save()
                        except Exception as e:
                            print(c, e)
                            print(row[column], ' not in builder table')

                            try:
                                c.person_fk = Person.objects.get(wikitextslug=row[column])
                                c.save()
                                print(row[column], ' is in person table and has been saved')
                            except ObjectDoesNotExist:
                                print(row[column], ' not in person table')

                                try:
                                    c.company_fk = Company.objects.get(wikislug=row[column])
                                    c.save()
                                    print(row[column], ' is in company table and has been saved')
                                except:
                                    print(row[column], ' not in company table')
                                    continue